from CheckmarxPythonSDK.CxOne import (
    update_package_state,
    update_package_state_bulk,
    update_supply_chain_risk,
    update_supply_chain_risks_bulk,
)
from CheckmarxPythonSDK.CxOne.dto import (
    BulkPackageEntry,
    BulkSupplyChainRiskEntry,
    PackageAction,
    PackageActionValue,
    SupplyChainRiskAction,
    UpdatePackageStateBulkRequest,
    UpdatePackageStateRequest,
    UpdateSupplyChainRiskRequest,
    UpdateSupplyChainRisksBulkRequest,
)


def test_update_package_state_muted():
    request = UpdatePackageStateRequest(
        packageName="@babel/runtime",
        packageVersion="7.24.0",
        packageManager="Npm",
        projectId="b8401dbb-ae8f-43f6-bbd2-dd0aa53b66e6",
        actions=[
            PackageAction(
                actionType="Ignore",
                value=PackageActionValue(state="Muted"),
                comment="Mute via SDK test",
            )
        ],
    )
    result = update_package_state(request)
    assert result is True


def test_update_package_state_snooze():
    request = UpdatePackageStateRequest(
        packageName="@babel/runtime",
        packageVersion="7.24.0",
        packageManager="Npm",
        projectId="b8401dbb-ae8f-43f6-bbd2-dd0aa53b66e6",
        actions=[
            PackageAction(
                actionType="Ignore",
                value=PackageActionValue(
                    state="Snooze", endDate="2026-12-31T23:59:59.000Z"
                ),
                comment="Snooze via SDK test",
            )
        ],
    )
    result = update_package_state(request)
    assert result is True


def test_update_package_state_bulk():
    request = UpdatePackageStateBulkRequest(
        packagesProfile=[
            BulkPackageEntry(
                packageName="@babel/runtime",
                packageVersion="7.24.0",
                packageManager="Npm",
                projectId="b8401dbb-ae8f-43f6-bbd2-dd0aa53b66e6",
            ),
        ],
        actions=[
            PackageAction(
                actionType="Ignore",
                value=PackageActionValue(state="Muted"),
                comment="Bulk mute via SDK test",
            ),
        ],
    )
    result = update_package_state_bulk(request)
    assert result is True


def test_update_supply_chain_risk():
    request = UpdateSupplyChainRiskRequest(
        packageName="coa",
        packageVersion="3.1.3",
        packageManager="Npm",
        supplyChainRiskId="6057d4e5-4760-a3f8-c8e6-bf57a8505af5",
        projectIds=["b8401dbb-ae8f-43f6-bbd2-dd0aa53b66e6"],
        actions=[
            SupplyChainRiskAction(
                actionType="ChangeState",
                value="ToVerify",
                comment="Change state via SDK test",
            ),
            SupplyChainRiskAction(
                actionType="ChangeScore",
                value=4,
                comment="Change score via SDK test",
            ),
        ],
    )
    result = update_supply_chain_risk(request)
    assert result is not None


def test_update_supply_chain_risks_bulk():
    request = UpdateSupplyChainRisksBulkRequest(
        packageSupplyChainRisks=[
            BulkSupplyChainRiskEntry(
                packageName="coa",
                packageVersion="3.1.3",
                packageManager="Npm",
                supplyChainRiskId="6057d4e5-4760-a3f8-c8e6-bf57a8505af5",
                projectIds=["b8401dbb-ae8f-43f6-bbd2-dd0aa53b66e6"],
            ),
        ],
        actions=[
            SupplyChainRiskAction(
                actionType="ChangeState",
                value="ToVerify",
                comment="Bulk change state via SDK test",
            ),
        ],
    )
    result = update_supply_chain_risks_bulk(request)
    assert result is not None


def test_update_package_state_monitored():
    request = UpdatePackageStateRequest(
        packageName="@babel/runtime",
        packageVersion="7.24.0",
        packageManager="Npm",
        projectId="b8401dbb-ae8f-43f6-bbd2-dd0aa53b66e6",
        actions=[
            PackageAction(
                actionType="Ignore",
                value=PackageActionValue(state="Monitored"),
                comment="Restore monitoring via SDK test",
            )
        ],
    )
    result = update_package_state(request)
    assert result is True
