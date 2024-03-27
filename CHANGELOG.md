# Changelog

## [0.9.0](https://github.com/ublue-os/yafti/compare/v0.8.0...v0.9.0) (2024-03-27)


### Features

* add PKGBUILD for Arch packaging ([#163](https://github.com/ublue-os/yafti/issues/163)) ([a827362](https://github.com/ublue-os/yafti/commit/a8273626e84e707e400212ca3d1d412cb85df019))
* **window:** Move "Next" button to top right ([#156](https://github.com/ublue-os/yafti/issues/156)) ([4abb8d4](https://github.com/ublue-os/yafti/commit/4abb8d42cde5cdc6b1eb13790cdd17a1772662ef))


### Bug Fixes

* Correct a spacing issue between preferred and package in text ([#183](https://github.com/ublue-os/yafti/issues/183)) ([57bcee5](https://github.com/ublue-os/yafti/commit/57bcee571a06c1bcaef3da5f8836a4f3e106c23c))
* Revert pydantic upgrade until required fixes can be made ([#184](https://github.com/ublue-os/yafti/issues/184)) ([1ff59d3](https://github.com/ublue-os/yafti/commit/1ff59d36ff81b2e71f774b404f66df4b256b1194))

## [0.8.0](https://github.com/ublue-os/yafti/compare/v0.7.1...v0.8.0) (2023-08-07)


### Features

* add save_state config property for changing when last-save state is recorded ([#145](https://github.com/ublue-os/yafti/issues/145)) ([0bc73af](https://github.com/ublue-os/yafti/commit/0bc73afe72d5b0a42a0e872efd07e1dbe2d6fb97))
* support for packages key for packages screen ([#148](https://github.com/ublue-os/yafti/issues/148)) ([381f73e](https://github.com/ublue-os/yafti/commit/381f73edbfff46a47cdf864593a2e762443738da))


### Bug Fixes

* pass state explicitly instead of overwriting id builtin ([#147](https://github.com/ublue-os/yafti/issues/147)) ([9fd3d79](https://github.com/ublue-os/yafti/commit/9fd3d7995d72b0364f4edfedfb147b764a40ac17))

## [0.7.1](https://github.com/ublue-os/yafti/compare/v0.7.0...v0.7.1) (2023-08-07)


### Bug Fixes

* support for multiple package screens in one config ([#139](https://github.com/ublue-os/yafti/issues/139)) ([c9db948](https://github.com/ublue-os/yafti/commit/c9db948fb84838676cc304023be43c97a215d6ba))

## [0.7.0](https://github.com/ublue-os/yafti/compare/v0.6.2...v0.7.0) (2023-07-05)


### Features

* Allow run plugin to be used as a package manager ([#128](https://github.com/ublue-os/yafti/issues/128)) ([7912e09](https://github.com/ublue-os/yafti/commit/7912e0984b6431f25482e681604944f2dc603215))


### Bug Fixes

* add application title ([#113](https://github.com/ublue-os/yafti/issues/113)) ([7f6b475](https://github.com/ublue-os/yafti/commit/7f6b4757632b4885eb882156c8e1f8e79711b070))


### Reverts

* "fix: add application title" ([#116](https://github.com/ublue-os/yafti/issues/116)) ([fb3c8ee](https://github.com/ublue-os/yafti/commit/fb3c8eee34548428efec7bf4f25883d39e76e23d))

## [0.6.2](https://github.com/ublue-os/yafti/compare/v0.6.1...v0.6.2) (2023-05-30)


### Bug Fixes

* move user data to sub-folder and ensure folder existence ([#102](https://github.com/ublue-os/yafti/issues/102)) ([7fce7fb](https://github.com/ublue-os/yafti/commit/7fce7fb7e1f1f4e82d359c4653494fcd0c4b593a))

## [0.6.1](https://github.com/ublue-os/yafti/compare/v0.6.0...v0.6.1) (2023-04-17)


### Bug Fixes

* multiple links in "final-screen" values results in error ([#84](https://github.com/ublue-os/yafti/issues/84)) ([457ffe8](https://github.com/ublue-os/yafti/commit/457ffe83865079c61101d0a2b705cd1485a7340b))
* yafti.screen.package title doesn't show up ([#85](https://github.com/ublue-os/yafti/issues/85)) ([8641b56](https://github.com/ublue-os/yafti/commit/8641b5614d89e28b912ae5a6fe0ba646f22c70ee))

## [0.6.0](https://github.com/ublue-os/yafti/compare/v0.5.0...v0.6.0) (2023-04-12)


### Features

* enable both user and system flatpak installs ([#82](https://github.com/ublue-os/yafti/issues/82)) ([8413bee](https://github.com/ublue-os/yafti/commit/8413beeadb5604407fa8a31e643c92fed29fbd7e))
* show a bouncing progress bar during package installation ([#74](https://github.com/ublue-os/yafti/issues/74)) ([e1fdd65](https://github.com/ublue-os/yafti/commit/e1fdd65d6cec405f1926524ed1e54c7319a8a147))

## [0.5.0](https://github.com/ublue-os/yafti/compare/v0.4.1...v0.5.0) (2023-03-27)


### Features

* extend title screen to include additional actions ([#66](https://github.com/ublue-os/yafti/issues/66)) ([a2fa984](https://github.com/ublue-os/yafti/commit/a2fa9848258b91c3f833a11751af1bf4c1a5bae2))

## [0.4.1](https://github.com/ublue-os/yafti/compare/v0.4.0...v0.4.1) (2023-03-24)


### Bug Fixes

* make sure bin entrypoint matches -m entrypoint ([#64](https://github.com/ublue-os/yafti/issues/64)) ([b2423b8](https://github.com/ublue-os/yafti/commit/b2423b81355496dde8b930ddeaaeca5d2eaf0baa))

## [0.4.0](https://github.com/ublue-os/yafti/compare/v0.3.1...v0.4.0) (2023-03-22)


### Features

* add logging mechanics & actual CLI ([#59](https://github.com/ublue-os/yafti/issues/59)) ([9df69c6](https://github.com/ublue-os/yafti/commit/9df69c6225f6d6b285182cdd5a65eb959fac8604))


### Documentation

* explain how to use yafti in a containerfile ([#58](https://github.com/ublue-os/yafti/issues/58)) ([8be1d27](https://github.com/ublue-os/yafti/commit/8be1d27965e1f5f6bb84a95f310f51fa83881cae))
* fix RUN command ([#61](https://github.com/ublue-os/yafti/issues/61)) ([8ed4232](https://github.com/ublue-os/yafti/commit/8ed4232dfc6ddd6759dd149bb17739fa3d196f19))

## [0.3.1](https://github.com/ublue-os/yafti/compare/v0.3.0...v0.3.1) (2023-03-20)


### Bug Fixes

* quit app when close requested ([#55](https://github.com/ublue-os/yafti/issues/55)) ([924a8aa](https://github.com/ublue-os/yafti/commit/924a8aaf1332e9dfe91157f352a35b55448d860f))

## [0.3.0](https://github.com/ublue-os/yafti/compare/v0.2.8...v0.3.0) (2023-03-20)


### Features

* add "first run" protections and configuration ([#46](https://github.com/ublue-os/yafti/issues/46)) ([290b06e](https://github.com/ublue-os/yafti/commit/290b06ee836421673410a6313234c7d2d45e15c1))
* add consent screen and screen conditions ([#47](https://github.com/ublue-os/yafti/issues/47)) ([4ff07c4](https://github.com/ublue-os/yafti/commit/4ff07c484f8f451978870c54a2db224dae8eb0f9))
* customize which groups are enabled by default ([#53](https://github.com/ublue-os/yafti/issues/53)) ([dfa363a](https://github.com/ublue-os/yafti/commit/dfa363a8a72f7b50ceb20870a7dc6890723bd3e2))


### Bug Fixes

* **deps:** lock pydantic dep to match fedora 38 ([#38](https://github.com/ublue-os/yafti/issues/38)) ([7dc7fac](https://github.com/ublue-os/yafti/commit/7dc7fac7a32d9edc54148e69abf02c35f569302e))
* **packaging:** use pyproject-rpm-macros ([#40](https://github.com/ublue-os/yafti/issues/40)) ([3885b89](https://github.com/ublue-os/yafti/commit/3885b892456036bca93a1cfb629754a4e772cf35))

## [0.2.8](https://github.com/ublue-os/yafti/compare/v0.2.7...v0.2.8) (2023-03-15)


### Bug Fixes

* **release:** restore upload-assets action ([#36](https://github.com/ublue-os/yafti/issues/36)) ([d021ae3](https://github.com/ublue-os/yafti/commit/d021ae339346980251c3f1f0f19fdde9c070e877))

## [0.2.7](https://github.com/ublue-os/yafti/compare/v0.2.6...v0.2.7) (2023-03-15)


### Bug Fixes

* **release:** rpm version needs to be dynamic ([#34](https://github.com/ublue-os/yafti/issues/34)) ([c3c06d4](https://github.com/ublue-os/yafti/commit/c3c06d4210472d441a77ffd3718217d370fb5be9))

## [0.2.6](https://github.com/ublue-os/yafti/compare/v0.2.5...v0.2.6) (2023-03-15)


### Bug Fixes

* **release:** replace release upload action ([#32](https://github.com/ublue-os/yafti/issues/32)) ([e5ae2d2](https://github.com/ublue-os/yafti/commit/e5ae2d2132982d4185960d33331ab08bf769f1c2))

## [0.2.5](https://github.com/ublue-os/yafti/compare/v0.2.4...v0.2.5) (2023-03-15)


### Bug Fixes

* **release:** adjust asset path to fit current model ([#30](https://github.com/ublue-os/yafti/issues/30)) ([dcf364b](https://github.com/ublue-os/yafti/commit/dcf364b7ad3300238c51790ca857587e88138d75))

## [0.2.4](https://github.com/ublue-os/yafti/compare/v0.2.3...v0.2.4) (2023-03-15)


### Bug Fixes

* **release:** supply file paths for artifacts ([#28](https://github.com/ublue-os/yafti/issues/28)) ([7b1e9ba](https://github.com/ublue-os/yafti/commit/7b1e9bac84acc35a5a05562cfc4b959cc2a4a695))

## [0.2.3](https://github.com/ublue-os/yafti/compare/v0.2.2...v0.2.3) (2023-03-15)


### Bug Fixes

* **release:** pass in tag reference on build ([#26](https://github.com/ublue-os/yafti/issues/26)) ([88d8850](https://github.com/ublue-os/yafti/commit/88d885062edb4c1f194869f9fcd77563276c11a9))

## [0.2.2](https://github.com/ublue-os/yafti/compare/v0.2.1...v0.2.2) (2023-03-15)


### Bug Fixes

* **release:** consolidate release process ([#24](https://github.com/ublue-os/yafti/issues/24)) ([6450bce](https://github.com/ublue-os/yafti/commit/6450bceb5669f73c6105297932b70a4699a8c58c))

## [0.2.1](https://github.com/ublue-os/yafti/compare/v0.2.0...v0.2.1) (2023-03-15)


### Bug Fixes

* **ci:** typo on workflow trigger ([#22](https://github.com/ublue-os/yafti/issues/22)) ([9e9c6a8](https://github.com/ublue-os/yafti/commit/9e9c6a833cf0834af43dd8d64138c8cec8706386))

## [0.2.0](https://github.com/ublue-os/yafti/compare/v0.1.0...v0.2.0) (2023-03-15)


### Features

* add RPM spec ([#12](https://github.com/ublue-os/yafti/issues/12)) ([3047cb5](https://github.com/ublue-os/yafti/commit/3047cb5ce6484a5df7348117951e33ab26661224))

## 0.1.0 (2023-03-13)


### Features

* add console screen component ([34f25fa](https://github.com/ublue-os/yafti/commit/34f25fae0c2f7534299043d25a6edf73f0582013))
* allow for package installation ([64e49a9](https://github.com/ublue-os/yafti/commit/64e49a9f424a9a4b8cc8ed0e395c19e008b15441))
* development and contrib documentation ([322ca9f](https://github.com/ublue-os/yafti/commit/322ca9f76e72ced437672d9648ed0d5da134774a))
* expland YaftiScreen definition ([1080107](https://github.com/ublue-os/yafti/commit/10801071c925cb2719ea8c5826ab62e6e16c7c7f))
* implement async support and some async methods ([eeb55ff](https://github.com/ublue-os/yafti/commit/eeb55ff97ae7696f43f1e8ae2be331c3ba604717))
* initial commit ([d85ab8a](https://github.com/ublue-os/yafti/commit/d85ab8af779649a0e0d95e53591f56c8b6e02a99))
* proper shutdown / closure ([7514d3a](https://github.com/ublue-os/yafti/commit/7514d3aeb2d92447470d156b02a4b93d4542b087))
* signals/observer and global button state ([3c45bb3](https://github.com/ublue-os/yafti/commit/3c45bb3897fd11a3bc95626a1272353e615f5028))
* start of unit tests ([135c934](https://github.com/ublue-os/yafti/commit/135c93449aec24a2e6d4b6db7be1424931570788))
* track screen state for packages ([2204e1d](https://github.com/ublue-os/yafti/commit/2204e1d4b23f8da5ade290e67451dca4d9afffa7))


### Bug Fixes

* add ruff for enhanced linting ([75daf97](https://github.com/ublue-os/yafti/commit/75daf970e9a5f79662e7963b74e0659223ca01c6))
* flatpack exec/install/remove ([2cefa20](https://github.com/ublue-os/yafti/commit/2cefa207ff9e177cc09a5f5ad806219e357fbc96))


### Documentation

* copyediting and formatting on the readme ([#6](https://github.com/ublue-os/yafti/issues/6)) ([d973098](https://github.com/ublue-os/yafti/commit/d9730989433446e78ebbb7d34817bf10deb5787a))
* improve developer instructions ([88a3a5e](https://github.com/ublue-os/yafti/commit/88a3a5ea0d9a0d3a41d802cd996eac4085cc3433))
