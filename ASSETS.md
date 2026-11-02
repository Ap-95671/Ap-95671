# Assets and maintenance

This profile uses local assets rather than live image endpoints from statistics services. The header and project covers are custom SVG artwork, with no scripts, external fonts or embedded remote resources. The Custerra logo was supplied by its creator/owner, who explicitly confirmed ownership. No application software licence is granted by this profile.

## Technology marks

Technology icons come from [Devicon](https://github.com/devicons/devicon), pinned to commit `32fe1d3b3f36ad11f90ab94f7db59738139c2bf6`. The upstream [MIT notice](assets/licenses/devicon-MIT.txt) is retained. Icons were placed on consistent neutral contrast tiles; the individual brand marks remain their owners’ property and do not imply endorsement. Only technologies supported by the actual projects are shown. C/C++, TensorFlow and PyTorch were not inferred from unrelated dependencies.

## Motion and accessibility

The custom typewriter header rotates four grounded phrases over 32 seconds. It contains an SVG reduced-motion rule and a static text version; the README also links the static asset. Native Markdown carries the essential introduction, status and links, so neither motion nor text inside a scaled image is required to understand the profile. Skill icons have accessible names; project descriptions remain normal wrapping text beneath the cover images.

## Contribution visuals

The contribution workflow uses only standard `ubuntu-24.04` runners in this public repository. Standard public-repository runner compute is free under [GitHub's current billing policy](https://docs.github.com/en/billing/concepts/product-billing/github-actions). No larger runner, paid card API or subscription is used. A tiny generated artifact is retained for one day; avoid accumulating artifacts or adding unrelated workflows.

The SVG-only [Platane/snk](https://github.com/Platane/snk) action is pinned to a reviewed immutable commit. Its generator job has `contents: read`; it receives only this repository's ephemeral token and fetches the GitHub contribution calendar. It does not receive a personal access token or access to Custerra/private project contents. A separate publisher job has `contents: write` and runs only the checked-in allowlisted publisher. It validates and publishes four generated files in one fast-forward commit; no history rewrite or application deployment occurs.

The schedule is weekly, Monday at 04:23 UTC, plus manual dispatch. The static snapshot records its actual generated date and GitHub-reported counts; it is a snapshot, not a performance score. No private repository names, source code or personal contact data are requested by the calendar query. GitHub controls what the calendar exposes.

When updating dependencies, review the upstream source and replace full action SHAs deliberately. If a run fails, existing assets remain in place; do not replace them with broken URLs or invented data. Review the Actions run before claiming refresh success. The profile needs no continuously running server.
