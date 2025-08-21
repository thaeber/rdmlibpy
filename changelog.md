<!-- insertion marker -->

<a name="v0.2.24"></a>

## [v0.2.24](https://github.com/thaeber/rdmlibpy/compare/v0.2.23...v0.2.24) (2025-08-21)

### Features

- Allows configuration of the merge method for attributes. ([c4111cb](https://github.com/thaeber/rdmlibpy/commit/c4111cb43cfd4f8bf8dc91a1ac01a67c9cd4e8fd))
- Select index range of `xarray` data structures ([e01da7a](https://github.com/thaeber/rdmlibpy/commit/e01da7a88cc835d54a99513357fc16b5c75fbfc7))

### Chore

- pre-commit run --all ([47fb700](https://github.com/thaeber/rdmlibpy/commit/47fb700c79f6b5d415a60eb3181ca37822f94033))

<a name="v0.2.23"></a>

## [v0.2.23](https://github.com/thaeber/rdmlibpy/compare/v0.2.22...v0.2.23) (2025-08-17)

### Bug Fixes

- Explicitly pass `keep_attrs=True` to `Dataset.map` in range selection ([0ebff37](https://github.com/thaeber/rdmlibpy/commit/0ebff374ba0652fb65ba243b81db46b85d81b084))
- Keep `DataArray` and `Dataset` attributes upon range selection ([15f8136](https://github.com/thaeber/rdmlibpy/commit/15f8136a7511130d8dab6643bf7395d11e308dc7))
- Avoid dim expansion in unrelated variables for range selection ([734f104](https://github.com/thaeber/rdmlibpy/commit/734f10480ff56489b0b465e664ba64fc0e117601))
- Remove internal `pint:quantify` attribute when loading cached data ([8df73d7](https://github.com/thaeber/rdmlibpy/commit/8df73d73734f85f803eec446e21643d3aac1ebe9))
- Keep attributes in xarray transforms ([2d35c75](https://github.com/thaeber/rdmlibpy/commit/2d35c75562934f63990218f9c21b389c8f5b441a))

### Features

- Create `xarray.DataTree` ([40f9e42](https://github.com/thaeber/rdmlibpy/commit/40f9e42c0b26e45a6c220b7e267cada381ce3ba0))
- Merge transform for `xarray.Dataset` ([fc93d21](https://github.com/thaeber/rdmlibpy/commit/fc93d2139cc5be340dfd3a2bbd2b6c5e6ce2b4fa))
- Dequantify `xarray` objects with explicit units and move units to attributes ([69fd9e4](https://github.com/thaeber/rdmlibpy/commit/69fd9e437e80bd1b6364605dc687259707e309be))
- By default `XarrayUnits` will now only set the `units` attribute ([743fc73](https://github.com/thaeber/rdmlibpy/commit/743fc73ed5a2755ba77a4d3459eecd875b22a97d))
- Include data from another YAML file into the workflow ([8a557e9](https://github.com/thaeber/rdmlibpy/commit/8a557e9010b288add0cda8003caa21915fd7d667))
- Convert `pandas.DataFrame` to `xarray.Dataset` ([5511bbe](https://github.com/thaeber/rdmlibpy/commit/5511bbec6f0814e3a476c197678935326dc70eaa))
- Swap dimensions for `xarray.DataArray` and `xarray.Dataset` ([c195656](https://github.com/thaeber/rdmlibpy/commit/c1956564fbfa63902eae0bd584b0128bdb019e3c))
- ScalarSource process node ([b06a067](https://github.com/thaeber/rdmlibpy/commit/b06a06794f35e110e833d8942928b6426bf459d9))
- Add XArrayAssign transform with unit tests for variable assignment ([e160402](https://github.com/thaeber/rdmlibpy/commit/e1604028a9d8132d27e477f752129f8b7100dbed))
- Add XArraySelectVariable transform ([109b76e](https://github.com/thaeber/rdmlibpy/commit/109b76e9eb6c66843f4876f8dc0291a9325c14ea))
- Introduce XArraySelectRange and refactor XArraySelectTimespan for improved selection functionality ([e9567bb](https://github.com/thaeber/rdmlibpy/commit/e9567bbe1cdb80a22f32ce97e8cc49c28064f12c))
- Enhance XArrayAffineTransform to accept optional matrix and dimensions ([32ee179](https://github.com/thaeber/rdmlibpy/commit/32ee1790680d5ea07dea59686065ae36165bc4ae))
- Affine transform for `xarray` data array and dataset ([824e44a](https://github.com/thaeber/rdmlibpy/commit/824e44ab93a83135e7715e9840cceb448b0e064b))

### Code Refactoring

- Renamed files related to dataframes to follow the scheme `dataframes._[module].py` ([448f80a](https://github.com/thaeber/rdmlibpy/commit/448f80a7fede98986b12e268dcf2bde3746af84f))

### Chore

- pre-commit run --all ([39f60aa](https://github.com/thaeber/rdmlibpy/commit/39f60aad2ac065eb242075eace9c1739939316ef))

<a name="v0.2.22"></a>

## [v0.2.22](https://github.com/thaeber/rdmlibpy/compare/v0.2.21...v0.2.22) (2025-08-15)

### Features

- Mean values transform for `xarray` data arrays and datasets ([3969e3a](https://github.com/thaeber/rdmlibpy/commit/3969e3a55252c0881ccf044cb607fb1eb1d0708f))
- Squeeze transform fo `xarray` data arrays or datasets ([2d7d640](https://github.com/thaeber/rdmlibpy/commit/2d7d6401dd7c135ecd521bc3eb52172eb2b39af4))

### Chore

- pre-commit run --all ([30358f7](https://github.com/thaeber/rdmlibpy/commit/30358f7c1e0b366c14e1e39d6d414f0f23cbdce7))

<a name="v0.2.21"></a>

## [v0.2.21](https://github.com/thaeber/rdmlibpy/compare/v0.2.20...v0.2.21) (2025-04-10)

### Features

- Enable loading all spectral types in Bruker files ([e2b59b0](https://github.com/thaeber/rdmlibpy/commit/e2b59b0ad939bf456a868bd46967a9a622980422))

<a name="v0.2.20"></a>

## [v0.2.20](https://github.com/thaeber/rdmlibpy/compare/v0.2.19...v0.2.20) (2025-03-29)

### Bug Fixes

- timespan conversion and add test (#27) ([507a815](https://github.com/thaeber/rdmlibpy/commit/507a8156d26791bd66238e0a6687938a6c3d7fdd))

<a name="v0.2.19"></a>

## [v0.2.19](https://github.com/thaeber/rdmlibpy/compare/v0.2.18...v0.2.19) (2025-03-28)

### Features

- Metadata resolvers to calculate timedelta values from timestamps ([f8163ac](https://github.com/thaeber/rdmlibpy/commit/f8163ac17a09657e0efb8dabee198e67d0f98e57))

<a name="v0.2.18"></a>

## [v0.2.18](https://github.com/thaeber/rdmlibpy/compare/v0.2.17...v0.2.18) (2025-03-13)

### Features

- Exposing underlying metadata container for direct access of source data ([334ecb8](https://github.com/thaeber/rdmlibpy/commit/334ecb885581326c0a87bd040e2d24ea78395c99))

<a name="v0.2.17"></a>

## [v0.2.17](https://github.com/thaeber/rdmlibpy/compare/v0.2.16...v0.2.17) (2025-03-10)

### Features

- File cache for `xarray.DataTree` ([b498bf5](https://github.com/thaeber/rdmlibpy/commit/b498bf5c7714d7a218c118c30a77b25a1421692a))

<a name="v0.2.16"></a>

## [v0.2.16](https://github.com/thaeber/rdmlibpy/compare/v0.2.15...v0.2.16) (2025-03-09)

### Features

- Create workflow from sequence of process instances ([9a1f4ea](https://github.com/thaeber/rdmlibpy/commit/9a1f4ea61b182c42441ad676d56ea4160c603c48))

### Code Refactoring

- Derive `ProcessNode` and `ProcessParam` from `pydantic.BaseModel` (#26) ([4014fbc](https://github.com/thaeber/rdmlibpy/commit/4014fbc30c5a778c7282bb7f2df71067e1334ca8))

### Chore

- pre-commit run --all ([5fe1ac2](https://github.com/thaeber/rdmlibpy/commit/5fe1ac24c60bed05d7f505a5c4dea80e260b04ba))

<a name="v0.2.15"></a>

## [v0.2.15](https://github.com/thaeber/rdmlibpy/compare/v0.2.14...v0.2.15) (2025-03-06)

### Bug Fixes

- Avoid `pint.quantify`on cache read when no pint units present ([a3ccbf2](https://github.com/thaeber/rdmlibpy/commit/a3ccbf2814907dfe32971d412675837a302b7a5c))

### Features

- Calling `Cache.run` writes and returns cached value without being part of a process workflow ([c461f0f](https://github.com/thaeber/rdmlibpy/commit/c461f0ff780d9126740f8d330cd8367ea28e09bd))

### Code Refactoring

- Renamed `_run` to `_run_with_node` ([a267a2e](https://github.com/thaeber/rdmlibpy/commit/a267a2eaa50e7e95ccfd6ee1d176d6c160203f51))

<a name="v0.2.14"></a>

## [v0.2.14](https://github.com/thaeber/rdmlibpy/compare/v0.2.13...v0.2.14) (2025-02-21)

### Bug Fixes

- Avoid passing indexers of type `str` to sequence containers ([4c4e94d](https://github.com/thaeber/rdmlibpy/commit/4c4e94d14e8c389e2f93789ab8698730ecb78386))

<a name="v0.2.13"></a>

## [v0.2.13](https://github.com/thaeber/rdmlibpy/compare/v0.2.12...v0.2.13) (2025-02-21)

### Bug Fixes

- Raise `AttributeError` instead of `KeyError` when a key/attribute is not found ([230b06d](https://github.com/thaeber/rdmlibpy/commit/230b06d5c2785217640f93c60314e9cad90b2a9a))

### Chore

- pre-commit run --all ([3d7c123](https://github.com/thaeber/rdmlibpy/commit/3d7c1233c3ca859d3897947a9abb87ade436bde2))

<a name="v0.2.12"></a>

## [v0.2.12](https://github.com/thaeber/rdmlibpy/compare/v0.2.11...v0.2.12) (2025-02-19)

### Features

- Loader (davis.image_set) for importing DaVis image sets ([4326c69](https://github.com/thaeber/rdmlibpy/commit/4326c6904ee7e44bc70c4717636eff77196eefe3))
- Allow parameterization of the time coding when writing netcdf files as cache ([33f9317](https://github.com/thaeber/rdmlibpy/commit/33f9317da6d264188a557b8c57231e1b89047f06))

<a name="v0.2.11"></a>

## [v0.2.11](https://github.com/thaeber/rdmlibpy/compare/v0.2.10...v0.2.11) (2025-02-18)

### Bug Fixes

- Provide an explicit unit & dtype to ensure correct encoding of times for chunked arrays ([7b1ecbd](https://github.com/thaeber/rdmlibpy/commit/7b1ecbd3808d1385be335dae95c344bd15d0f88b))
- Tests of xarray file cache now actually use variables of type `np.datetime64` ([223af2b](https://github.com/thaeber/rdmlibpy/commit/223af2b4a79bafaf82a5ac4696bd5cac88295c00))

<a name="v0.2.10"></a>

## [v0.2.10](https://github.com/thaeber/rdmlibpy/compare/v0.2.9...v0.2.10) (2025-02-18)

### Features

- Optionally only open a `xarray.Dataset` when loading from cache and to provide a `chunks` size ([7338b2e](https://github.com/thaeber/rdmlibpy/commit/7338b2ead3f2ecca653d8c7b7f8ce349364bc6e7))

<a name="v0.2.9"></a>

## [v0.2.9](https://github.com/thaeber/rdmlibpy/compare/v0.2.8...v0.2.9) (2025-02-18)

### Bug Fixes

- __repr__ will now resolve interpolations for better inspection ([2d6ad18](https://github.com/thaeber/rdmlibpy/commit/2d6ad181274205da188c0fd55202d2fcd8dafab6))

### Features

- Add convenient top level query functions `find` and `defines` ([b14b258](https://github.com/thaeber/rdmlibpy/commit/b14b258acc7d53e99deb0b445058533a8377d0b4))

<a name="v0.2.8"></a>

## [v0.2.8](https://github.com/thaeber/rdmlibpy/compare/v0.2.7...v0.2.8) (2025-02-11)

### Bug Fixes

- Error in `test_encoding_utf16` ([7f20523](https://github.com/thaeber/rdmlibpy/commit/7f205237906287b3b00065a4df380ddc95dbe707))

### Features

- Coerce invalid date/time values to NaT ([3890e1f](https://github.com/thaeber/rdmlibpy/commit/3890e1f0ffae59a14e21c164abf2d4b5cc253eac))

### Chore

- git-changelog -B patch ([a541ad7](https://github.com/thaeber/rdmlibpy/commit/a541ad7fbfae52018fba389eaeb310368a37c33f))

<a name="v0.2.7"></a>

## [v0.2.7](https://github.com/thaeber/rdmlibpy/compare/v0.2.6...v0.2.7) (2025-02-11)

### Features

- Optional encoding and thousands separator in `DataFrameReadCSV` ([217466d](https://github.com/thaeber/rdmlibpy/commit/217466d153ae2f070acea27fcc7f513aaf23239a))

### Chore

- git-changelog -B patch ([7175eb9](https://github.com/thaeber/rdmlibpy/commit/7175eb9fba9e781ceeabc899bb7760ceeee892b8))
- pre-commit run --all ([626f52c](https://github.com/thaeber/rdmlibpy/commit/626f52c76a68a72697eab1e3248be23e9b4451b1))

<a name="v0.2.6"></a>

## [v0.2.6](https://github.com/thaeber/rdmlibpy/compare/v0.2.5...v0.2.6) (2025-02-02)

### Features

- Updating dependencies ([7aa092a](https://github.com/thaeber/rdmlibpy/commit/7aa092acb27367fac25b389584c4803bbb3a9430))

<a name="v0.2.5"></a>

## [v0.2.5](https://github.com/thaeber/rdmlibpy/compare/v0.2.4...v0.2.5) (2024-11-19)

### Features

- Apply time offset to dataframe column (#25) ([724636b](https://github.com/thaeber/rdmlibpy/commit/724636b956650f74786187c1078562126074c3d2))

### Chore

- git-changelog -B patch ([c8b7218](https://github.com/thaeber/rdmlibpy/commit/c8b721825e56e78b373346032f803991cab153c1))
- pre-commit run --all ([e24ace4](https://github.com/thaeber/rdmlibpy/commit/e24ace42ba247e78b6f668b29fdb25199d92df50))

<a name="v0.2.4"></a>

## [v0.2.4](https://github.com/thaeber/rdmlibpy/compare/v0.2.3...v0.2.4) (2024-11-19)

### Features

- Forward or backward fill of non-numeric data in dataframe join (#24) ([1492cc5](https://github.com/thaeber/rdmlibpy/commit/1492cc575a83d85dc756ae031331be751c2f89f6))

### Chore

- git-changelog -B patch ([5c26725](https://github.com/thaeber/rdmlibpy/commit/5c267257b4d702c743aff74f71b58d0ae7f0ff46))
- pre-commit run --all ([e8b58f9](https://github.com/thaeber/rdmlibpy/commit/e8b58f9bde2baeadf03a0aba365de0773526a86e))

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
