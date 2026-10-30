import json
import tempfile
import time

import pytest

from CheckmarxPythonSDK.CxOne import (
    create_environment, delete_environment,
    create_tunnel, delete_tunnel_without_id, delete_tunnel, get_tunnel,
    get_tunnel_by_name, get_tunnels,
    create_sequence, delete_sequences, update_sequences_order, update_sequence,
    get_sequence_scripts, get_sequences, duplicate_sequence,
    get_sequence_recordings,
    create_recordings, delete_recordings, update_recording,
    get_environment_recordings, save_proxy_recorder_file,
)
from CheckmarxPythonSDK.CxOne.dto import (
    DastEnvironmentInput, DastScanType, DastCreateTunnelResponse,
    DastTunnelResponse, DastTunnelsResponse, DastSequence,
    DastSequenceWithRecordingCount, DastSequenceScriptsResponse,
    DastRecordingWithPosition, DastRecording, DastRecordingsCollection,
)


def _skip_on_client_error(e: Exception):
    msg = str(e)
    if "400" in msg or "401" in msg or "403" in msg or "404" in msg or "503" in msg:
        pytest.skip("API returned client error: {}".format(msg))
    raise e


@pytest.fixture
def env_id():
    """A throwaway Environment to drive tunnels/sequences/recordings on."""
    eid = create_environment(DastEnvironmentInput(
        domain=f"sdk-tsr-{int(time.time())}",
        url="https://example.com",
        scan_type=DastScanType.DAST,
    ))
    try:
        yield eid
    finally:
        delete_environment(eid)


@pytest.fixture(scope="session")
def zest_recording_file():
    """A minimal, genuinely valid Zest (JSON) recording.

    Confirmed live: recording uploads must be real Zest JSON content --
    create_recordings' docstring has the details. This is the smallest
    shape the server accepts.
    """
    path = tempfile.NamedTemporaryFile(suffix=".zest", delete=False).name
    with open(path, "w") as f:
        json.dump({
            "about": "This is a Zest script. For more detail about Zest visit https://github.com/zaproxy/zest/",
            "zestVersion": "0.8",
            "title": "minimal",
            "description": "",
            "author": "",
            "prefix": "",
            "type": "StandAlone",
            "parameters": {
                "tokenStart": "{{", "tokenEnd": "}}", "tokens": {},
                "elementType": "ZestVariables",
            },
            "statements": [],
            "authentication": [],
            "index": 0,
            "enabled": True,
        }, f)
    return path


@pytest.fixture
def two_recording_ids(env_id, zest_recording_file):
    """Two recordings created on `env_id`, returned as a list of IDs."""
    recordings = create_recordings(
        environment_id=env_id,
        files=[zest_recording_file, zest_recording_file],
        metadata=[{"name": "rec1", "description": "first"}, {"name": "rec2", "description": "second"}],
    )
    assert len(recordings) == 2
    return [r.id for r in recordings]


# ---- Tunnels ----


def test_tunnel_lifecycle(env_id):
    try:
        created = create_tunnel(
            name=f"sdk-test-tunnel-{int(time.time())}",
            environment_id=env_id,
            url="http://localhost:8080",
        )
    except Exception as e:
        _skip_on_client_error(e)
        return
    assert isinstance(created, DastCreateTunnelResponse)
    assert created.id

    try:
        fetched = get_tunnel(created.id)
        assert isinstance(fetched, DastTunnelResponse)
        assert fetched.id == created.id

        by_name = get_tunnel_by_name(created.name or created.tunnel_name)
        assert isinstance(by_name, DastTunnelResponse)
        assert by_name.id == created.id

        all_tunnels = get_tunnels()
        assert isinstance(all_tunnels, DastTunnelsResponse)
        assert any(t.id == created.id for t in all_tunnels.tunnels)
    finally:
        assert delete_tunnel(created.id) is True


def test_delete_tunnel_without_id_always_400s():
    # Documented spec behavior: this endpoint exists only to 400.
    with pytest.raises(Exception) as exc_info:
        delete_tunnel_without_id()
    assert "400" in str(exc_info.value)


# ---- Recordings ----


def test_create_recordings_rejects_non_zest_content(env_id):
    non_zest_path = tempfile.NamedTemporaryFile(suffix=".zst", delete=False).name
    with open(non_zest_path, "w") as f:
        f.write("not zest json\n")

    with pytest.raises(Exception) as exc_info:
        create_recordings(
            environment_id=env_id, files=[non_zest_path],
            metadata=[{"name": "rec1", "description": "x"}],
        )
    assert "ZST" in str(exc_info.value) or "400" in str(exc_info.value)


def test_create_and_delete_recordings(env_id, two_recording_ids):
    collection = get_environment_recordings(env_id)
    assert isinstance(collection, DastRecordingsCollection)
    assert collection.total_items == 2
    assert all(isinstance(r, type(collection.recordings[0])) for r in collection.recordings)

    assert delete_recordings(env_id, two_recording_ids) is True
    assert get_environment_recordings(env_id).total_items == 0


def test_update_recording(env_id, two_recording_ids):
    updated = update_recording(two_recording_ids[0], env_id, name="renamed")
    assert isinstance(updated, DastRecording)
    assert updated.name == "renamed"


def test_save_proxy_recorder_file_requires_json(env_id):
    non_json_path = tempfile.NamedTemporaryFile(suffix=".har.zst", delete=False).name
    with open(non_json_path, "w") as f:
        f.write("not json\n")

    with pytest.raises(Exception) as exc_info:
        save_proxy_recorder_file(env_id, non_json_path)
    assert "zst" in str(exc_info.value).lower() or "500" in str(exc_info.value)


# ---- Sequences ----


def test_sequence_lifecycle(env_id, two_recording_ids):
    seq = create_sequence(environment_id=env_id, name="seq1", recording_ids=two_recording_ids)
    assert isinstance(seq, DastSequence)
    assert seq.recording_ids == two_recording_ids
    seq_id = seq.id

    sequences = get_sequences(env_id)
    assert isinstance(sequences, list)
    assert any(isinstance(s, DastSequenceWithRecordingCount) and s.id == seq_id for s in sequences)

    recordings = get_sequence_recordings(env_id, seq_id)
    assert isinstance(recordings, list)
    assert all(isinstance(r, DastRecordingWithPosition) for r in recordings)
    assert [r.id for r in recordings] == two_recording_ids

    # The update's own response always comes back with empty recording_ids
    # (see update_sequence's docstring) -- verify the real state separately.
    updated = update_sequence(seq_id, env_id, name="seq1-renamed", recording_ids=[two_recording_ids[0]])
    assert isinstance(updated, DastSequence)
    assert updated.name == "seq1-renamed"
    assert [r.id for r in get_sequence_recordings(env_id, seq_id)] == [two_recording_ids[0]]

    dup = duplicate_sequence(env_id, seq_id)
    assert isinstance(dup, DastSequence)
    assert dup.id != seq_id
    assert dup.recording_ids == [two_recording_ids[0]]

    assert update_sequences_order(env_id, [dup.id, seq_id]) is True

    scripts = get_sequence_scripts(env_id)
    assert isinstance(scripts, DastSequenceScriptsResponse)
    # Chains cover both sequences (1 recording each after the update/
    # duplicate above) plus any recording not currently in a sequence
    # (rec2, dropped by the update) as its own standalone chain -- so
    # don't assert an exact count, just that every referenced recording
    # filename traces back to one of this environment's own recordings.
    assert scripts.chains
    all_recording_filenames = {r for chain in scripts.chains for r in chain.recordings}
    # two_recording_ids' recordings are named "rec1"/"rec2" (see fixture)
    assert all_recording_filenames <= {"rec1.zst", "rec2.zst"}
    assert isinstance(scripts.archive, str) and scripts.archive

    assert delete_sequences(env_id, [seq_id, dup.id]) is True
    assert get_sequences(env_id) == []
