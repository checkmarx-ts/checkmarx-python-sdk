# Changelog fragments

Do **not** edit `CHANGELOG.md` in a feature/fix PR -- every PR adding lines to
the same `Unreleased` block conflicts with every other one. Instead add one
small file here per PR:

    changelog.d/<short-topic>.md

Its content is one or more bullet lines, each starting with a tag:

    * [Add] DiscoveryAPI.get_orgs_coverage (GET /api/discovery/v2/orgs/coverage) -- ...
    * [Fix] RepoOrg crashed with TypeError on ... 

Tags: `[Breaking]`, `[Change]`, `[Add]`, `[Fix]`, `[Document]`.
Use a file name unique to your PR (the topic, not a counter) so two PRs never
touch the same file.

## At release time

The version-bump PR runs

    python scripts/release_changelog.py 1.9.5

which moves every fragment (and any legacy `Unreleased` block) into
`CHANGELOG.md` under `1.9.5 - <today>`, ordered Breaking, Change, Add, Fix,
Document, and deletes the fragment files. Use `--date YYYY-MM-DD` to override
the date and `--dry-run` to print the result without writing.
