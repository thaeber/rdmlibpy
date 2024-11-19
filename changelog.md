<!-- insertion marker -->

<a name="v0.2.3"></a>

## [v0.2.3](https://github.com/thaeber/rdmlibpy/compare/v0.2.2...v0.2.3) (2024-11-04)

### Bug Fixes

- By default sort Opus spectra by timestamp ([5b65d1d](https://github.com/thaeber/rdmlibpy/commit/5b65d1d3b09c70a94f312e95dba41a3f03dcaa31))

<a name="v0.2.2"></a>

## [v0.2.2](https://github.com/thaeber/rdmlibpy/compare/v0.2.1...v0.2.2) (2024-11-04)

### Bug Fixes

- Use descriptive name for spectral type when loading Opus spectra ([85e490b](https://github.com/thaeber/rdmlibpy/commit/85e490bbbf8e674af5b1c10fff06662c600c20f3))

### Chore

- git-changelog --bump=auto ([8f0de63](https://github.com/thaeber/rdmlibpy/commit/8f0de63602e149866668d3a76e3005d172b90732))

<a name="v0.2.1"></a>

## [v0.2.1](https://github.com/thaeber/rdmlibpy/compare/v0.2.0...v0.2.1) (2024-11-03)

### Bug Fixes

- Missing import and registration of xarray processes ([cf7ba91](https://github.com/thaeber/rdmlibpy/commit/cf7ba91eb18cdbdbf1823336739c928266a9cb77))

### Chore

- git-changelog --bump=auto ([7008518](https://github.com/thaeber/rdmlibpy/commit/700851807b066c0080066239f8e2dc2c55562bf8))
- pre-commit run -a ([eefc63c](https://github.com/thaeber/rdmlibpy/commit/eefc63c52537c23648df50cec3be64731177b8a4))

<a name="v0.2.0"></a>

## [v0.2.0](https://github.com/thaeber/rdmlibpy/compare/v0.1.12...v0.2.0) (2024-11-03)

### Features

- Cache nested dicts in xarray attributes (#23) ([cfbc266](https://github.com/thaeber/rdmlibpy/commit/cfbc2665abbc943fd85a4fa4f859c55cbac02186))
- Utility function to flatten and rebuilding nested dicts (#22) ([0517073](https://github.com/thaeber/rdmlibpy/commit/0517073d5d511a07e5c939e15d329dc3dececb51))
- File cache for xarray objects (DataArray & Dataset) (#21) ([c26381a](https://github.com/thaeber/rdmlibpy/commit/c26381aedd33469d36398947963b5eab4722e5d2))
- Set units and attributes on xarray objects (#20) ([86fd515](https://github.com/thaeber/rdmlibpy/commit/86fd51511ba144aa4894d687987bd00d3040814b))
- Select timespan in xarray (#19) ([4e718a1](https://github.com/thaeber/rdmlibpy/commit/4e718a133bdbdf568be26fcf98cfd4e5137f3a97))
- Basic loader for Bruker OPUS files (#18) ([2db5344](https://github.com/thaeber/rdmlibpy/commit/2db5344e44ecf50a37be45a0d9fdf8974559f8ed))

### Chore

- git-changelog -b ([59bbce1](https://github.com/thaeber/rdmlibpy/commit/59bbce106bda6bdb3b00a3c55c700d0282dc3b8f))
- pre-commit run -a ([0c2e71c](https://github.com/thaeber/rdmlibpy/commit/0c2e71c0ae45286274bf2cc52778ac3978b933ff))
- Explicit usage of pint_xarray to avoid it being stripped in pre-commit hook ([de394fa](https://github.com/thaeber/rdmlibpy/commit/de394fa8a4906264ecae2c8a042ab62d8b5cb403))

<a name="v0.1.12"></a>

## [v0.1.12](https://github.com/thaeber/rdmlibpy/compare/v0.1.11...v0.1.12) (2024-06-28)

### Bug Fixes

- Pandas 3.0 deprecation warning ([e7c588a](https://github.com/thaeber/rdmlibpy/commit/e7c588a6b3b490dda8af9b5bf431285e678e4539))

### Chore

- Updated changelog and running pre-commit ([0bedc7d](https://github.com/thaeber/rdmlibpy/commit/0bedc7d8b8539d45bf335a8ee651862e83efccb3))

<a name="v0.1.11"></a>

## [v0.1.11](https://github.com/thaeber/rdmlibpy/compare/v0.1.10...v0.1.11) (2024-06-22)

### Features

- Channel Eurotherm V1.1 includes power output ([5280b83](https://github.com/thaeber/rdmlibpy/commit/5280b83c23e9589e2fbf8fc1bc975d1e5f9c5bfc))

<a name="v0.1.10"></a>

## [v0.1.10](https://github.com/thaeber/rdmlibpy/compare/v0.1.9...v0.1.10) (2024-05-16)

### Bug Fixes

- Accessing metadata with an invalid key will now raise KeyError ([61ebdf5](https://github.com/thaeber/rdmlibpy/commit/61ebdf5ef6dd79dc0b93bdf6c8a1438d39a743c2))
- Converting metadata nodes to regular python objects before running a process ([dd88efb](https://github.com/thaeber/rdmlibpy/commit/dd88efb331e7a3064978c800d70eb050f383b1fa))
- Missing import of load_yaml function ([ced94c7](https://github.com/thaeber/rdmlibpy/commit/ced94c75065d380d9f8a4033c688c791d2876bf0))

### Features

- Metadata resolver to subtract a given timedelta value from a timestamp ([902baa7](https://github.com/thaeber/rdmlibpy/commit/902baa731f6debc33cb33b6efa2d41c6453a5bf6))
- Exclude private keys from metadata queries ([43fa699](https://github.com/thaeber/rdmlibpy/commit/43fa69913c6734b9644890ef4ee4aeed752d1683))
- Supporting in and not in operators on metadata ([946efac](https://github.com/thaeber/rdmlibpy/commit/946efaccaf8b9bb9cf16462a745ba829618a596a))
- Added convenience function load_yaml to load metadata ([cd99ec3](https://github.com/thaeber/rdmlibpy/commit/cd99ec3c34d4c505c4adf1f4e67335e72c8c237a))
- Adding metadata classes and queries to rdmlib (#10) ([78ea382](https://github.com/thaeber/rdmlibpy/commit/78ea382e23b612c535a1d2b9a60eced58f7e7359))

### Code Refactoring

- Define constants for recurring mapping keys ([7dcfd89](https://github.com/thaeber/rdmlibpy/commit/7dcfd8975a9383b1be8a37134be54127f579e1ff))
- Renamed test class to TestDataFrameFileCache ([ea06c9f](https://github.com/thaeber/rdmlibpy/commit/ea06c9fd0400448d205103f98d8d052b3a3cf83d))

### Chore

- Updating changelog.md ([4afb4e7](https://github.com/thaeber/rdmlibpy/commit/4afb4e7915dbbaae6b6b29bead08d468d22487c8))
- pre-commit run -a ([20436d1](https://github.com/thaeber/rdmlibpy/commit/20436d1bc0be0f5c94170ed8996e75e6afd3f1db))

<a name="v0.1.9"></a>

## [v0.1.9](https://github.com/thaeber/rdmlibpy/compare/v0.1.8...v0.1.9) (2024-04-29)

### Bug Fixes

- DataFrameWriteCSV -> Prevents blank lines from being written between rows of the data frame :bug: ([5825908](https://github.com/thaeber/rdmlibpy/commit/5825908276323d57a4d2b802d8b6cf86c53545f4))
- DataFrameWriteCSV => Fix writing attrs property when data frame contains pint columns :bug: ([f123de1](https://github.com/thaeber/rdmlibpy/commit/f123de1d0a741d87d29f1bc0e35f8f65b5e69507))
- Explicitly set utf-8 encoding when reading and writing text files :bug: ([7575ba0](https://github.com/thaeber/rdmlibpy/commit/7575ba04f1cfc9b38b92093f12f47ad2e714a9be))
- :bug: Explicitly set utf-8 encoding when reading and writing text files ([a2a9eff](https://github.com/thaeber/rdmlibpy/commit/a2a9effef583368f52b24fd55556a96ec50f011e))

### Chore

- Running pre-commit ([d3ce1b7](https://github.com/thaeber/rdmlibpy/commit/d3ce1b7b2c47cda099b7d3a832e0165ce9d475e0))
- Updated changelog ([df1c709](https://github.com/thaeber/rdmlibpy/commit/df1c70980ed6458f39a4030e6689418849bb2258))

<a name="v0.1.8"></a>

## [v0.1.8](https://github.com/thaeber/rdmlibpy/compare/v0.1.7...v0.1.8) (2024-04-28)

### Bug Fixes

- DataFrameFileCache => Preserve attrs when caching data frames ([483d9bb](https://github.com/thaeber/rdmlibpy/commit/483d9bbd39b8a191a446e8cbc9c802df9b0f4bf7))
- Create path to cache file if it does not exists ([80f7d17](https://github.com/thaeber/rdmlibpy/commit/80f7d17d2cb729637baa0efe81bf2e6bc6bbe897))
- Accidental return of dataframe without units when using dequantify=True ([45039d5](https://github.com/thaeber/rdmlibpy/commit/45039d50d16539bafdde22e920e8417b7eb8621b))
- Renamed "target" parameter to "filename" ([33d31e3](https://github.com/thaeber/rdmlibpy/commit/33d31e3011b78ab4999d8e7d21d781e2cc0840c3))
- Test for process id ([41203c0](https://github.com/thaeber/rdmlibpy/commit/41203c0169b2a6ce3ddf4a2c092b0566b29ed58c))
- Fixed typo in "dataframe.cache" process id (#9) ([f6acb32](https://github.com/thaeber/rdmlibpy/commit/f6acb32ef7c1026d6a1f4c0f956605ec1fc72d64))
- Renamed process to "dataframe.\[read|write\].csv" for consistency (#8) ([a9a7132](https://github.com/thaeber/rdmlibpy/commit/a9a7132bd19118838a1f4acbaf21b217692fd33b))
- DataFrameWriteCSV.run() did not return input value (#7) ([a297aa0](https://github.com/thaeber/rdmlibpy/commit/a297aa03a556fca1684b20fc2cda6c26855834cd))

### Features

- DataFrameWriteCSV => Write contents of attrs in the file header as comments ([c3f8da1](https://github.com/thaeber/rdmlibpy/commit/c3f8da14c14f2b4b1593deab076eb0e1fe7caf03))
- Storing metadata in the attrs dictionary of DataFrame ([8702ca8](https://github.com/thaeber/rdmlibpy/commit/8702ca8bbea2b76113b92b84479866927d9a1ba4))
- Automatic handling of data frames with units by default ([e8a02bb](https://github.com/thaeber/rdmlibpy/commit/e8a02bbd17caabd64ab0c1952d7f5d4a85c86d04))
- Added more granular handling of indices when writing to csv files. By default it now resets named indices before writing. ([0db9c17](https://github.com/thaeber/rdmlibpy/commit/0db9c17c5c2ba62f0f715709e2f461c9aa7d8d6a))

### Code Refactoring

- Renamed conda development environment to match package name ([59e098a](https://github.com/thaeber/rdmlibpy/commit/59e098afe94d64aae9ca46e4f08b4ffaf9cda896))

### Chore

- Adding and running pre-commit ([45f1b24](https://github.com/thaeber/rdmlibpy/commit/45f1b246393ad3ddf77b17327bf41d0d96231d8b))

<a name="v0.1.7"></a>

## [v0.1.7](https://github.com/thaeber/rdmlibpy/compare/v0.1.6...v0.1.7) (2024-04-23)

### Features

- Allow sequence of sequences when defining processes ([cf52463](https://github.com/thaeber/rdmlibpy/commit/cf524633b3708614ceda138c81d387c40f730b64))

### Chore

- Update changelog ([dcae5f0](https://github.com/thaeber/rdmlibpy/commit/dcae5f03fdabe0d8d153f73163bb610e9d4eb8ad))

<a name="v0.1.6"></a>

## [v0.1.6](https://github.com/thaeber/rdmlibpy/compare/v0.1.5...v0.1.6) (2024-04-23)

### Chore

- Update changelog ([2a066d7](https://github.com/thaeber/rdmlibpy/commit/2a066d71c1aad46d046bccff18123f00a16c86a9))
- Updated changelog ([b5ee656](https://github.com/thaeber/rdmlibpy/commit/b5ee6565c08dad644a411d8430320b0e951b40e9))

### Style

- Renamed project to "rdmlibpy" (#5) ([df40fa7](https://github.com/thaeber/rdmlibpy/commit/df40fa7494207692f01020649cc91599325adba8))

### Build

- Fixed invalid filename in bump-my-version config ([fc5a965](https://github.com/thaeber/rdmlibpy/commit/fc5a965e7c8a2960879a8807e8b4ba8cc37d5c30))

<a name="v0.1.5"></a>

## [v0.1.5](https://github.com/thaeber/rdmlibpy/compare/v0.1.3...v0.1.5) (2024-04-23)

### Style

- Renamed "select.\[columns|timespan\]" to "dataframe.select.\[columns|timespan\]" (#4) ([eb32028](https://github.com/thaeber/rdmlibpy/commit/eb320282b9696a6c1fbe45e44f76f00a84604603))

<a name="v0.1.3"></a>

## [v0.1.3](https://github.com/thaeber/rdmlibpy/compare/v0.1.2...v0.1.3) (2024-04-19)

<a name="v0.1.2"></a>

## [v0.1.2](https://github.com/thaeber/rdmlibpy/compare/v0.1.1...v0.1.2) (2024-04-02)

<a name="v0.1.1"></a>

## [v0.1.1](https://github.com/thaeber/rdmlibpy/compare/b6e05adfa1b72a75295601854b5caaedc1876993...v0.1.1) (2024-04-01)
