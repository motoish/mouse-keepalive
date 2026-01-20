# Changelog

## [1.2.5](https://github.com/motoish/mouse-keepalive/compare/mouse-keepalive-v1.2.4...mouse-keepalive-v1.2.5) (2026-01-19)


### Bug Fixes

* lint ([1e0494f](https://github.com/motoish/mouse-keepalive/commit/1e0494f82e133a7c98df7d53c89477a1cbc0fc64))
* modify log(with coordinates) ([0ab354e](https://github.com/motoish/mouse-keepalive/commit/0ab354ee86625c275729eeff191e879d57ced1fd))

## [1.2.4](https://github.com/motoish/mouse-keepalive/compare/mouse-keepalive-v1.2.3...mouse-keepalive-v1.2.4) (2026-01-19)


### Bug Fixes

* modify log ([4322ff3](https://github.com/motoish/mouse-keepalive/commit/4322ff3fdd803e7ee53bdbd643bf86b9416b8028))

## [1.2.3](https://github.com/motoish/mouse-keepalive/compare/mouse-keepalive-v1.2.2...mouse-keepalive-v1.2.3) (2026-01-19)


### Bug Fixes

* format python ([911a2bb](https://github.com/motoish/mouse-keepalive/commit/911a2bbf4409900195293198cba1ab1c53c9b6f9))
* **windows:** resolve output buffering issue causing delayed logs ([4c22550](https://github.com/motoish/mouse-keepalive/commit/4c22550932ea4fdbfe12dc8d20f500873b9e90c4))

## [1.2.2](https://github.com/motoish/mouse-keepalive/compare/mouse-keepalive-v1.2.1...mouse-keepalive-v1.2.2) (2026-01-15)


### Bug Fixes

* modify test_move_mouse.py ([1604d00](https://github.com/motoish/mouse-keepalive/commit/1604d00033ba07f08ec61ab1125993f714a5cede))
* optimize version configuration ([8c173bd](https://github.com/motoish/mouse-keepalive/commit/8c173bd080d041103a21557025a9b17c62f1ff33))

## [1.2.1](https://github.com/motoish/mouse-keepalive/compare/mouse-keepalive-v1.2.0...mouse-keepalive-v1.2.1) (2026-01-07)


### Bug Fixes

* lint ([867f5d4](https://github.com/motoish/mouse-keepalive/commit/867f5d4eab208b5d217e71727d665ebd19533fd2))
* optimize auto approve ([2508c51](https://github.com/motoish/mouse-keepalive/commit/2508c517ec5a78afbefe57e09cbb722274812dde))
* optimize auto approve ([6cf3258](https://github.com/motoish/mouse-keepalive/commit/6cf325868fb507195bd4d8ee24f246a8f35e9fd2))
* optimize auto approve ([871f082](https://github.com/motoish/mouse-keepalive/commit/871f082bd9c973c0d4e8828c183aae5010de683a))
* optimize ci ([408ad70](https://github.com/motoish/mouse-keepalive/commit/408ad70a0efbc7cf96d42c188293c8a5d3d10b28))
* optimize module ([ab10508](https://github.com/motoish/mouse-keepalive/commit/ab10508a3d16e5fb2f6053c18f6e9fecb7e8015d))
* optimize release workflow ([fb2acdf](https://github.com/motoish/mouse-keepalive/commit/fb2acdff0b639f6a0046ecedc9691b2ded573daa))
* optimize script and test ([a317173](https://github.com/motoish/mouse-keepalive/commit/a31717371c80910a8d04b367bbd9f9adc2f64c8a))
* optimize test ([96898a1](https://github.com/motoish/mouse-keepalive/commit/96898a13e2ca635e7dd146762cc1accbcf1fa48f))

## [1.2.0](https://github.com/motoish/mouse-keepalive/compare/mouse-keepalive-v1.1.0...mouse-keepalive-v1.2.0) (2026-01-07)


### Features

* add cross-platform executable builds for GitHub Releases ([d5c4601](https://github.com/motoish/mouse-keepalive/commit/d5c4601ed1283f08a6e49b220744ff5b8e47896a))
* add Makefile to simplify development commands ([39caf65](https://github.com/motoish/mouse-keepalive/commit/39caf654c63cd4c94191b9e447ce5d9f72644f22))
* integrate release-please for automated version management ([559c469](https://github.com/motoish/mouse-keepalive/commit/559c469a5a4df29d0b83e34681d47597fda72615))


### Bug Fixes

* add id-token permission ([375f380](https://github.com/motoish/mouse-keepalive/commit/375f380f9b36b2b841946625c9ccc7df2677e035))
* add mergify and modify README.md ([860bf14](https://github.com/motoish/mouse-keepalive/commit/860bf1477cdc1113edf448aee06f24908cb7d5aa))
* add release-please config-file and manifest-file ([aa59810](https://github.com/motoish/mouse-keepalive/commit/aa598102c708ce277f5d2ccb5e0f74f856577e48))
* improve release-please workflow and fix package name ([f9583bb](https://github.com/motoish/mouse-keepalive/commit/f9583bb0a37a132b3a2914295be236bafdedda2d))
* improve release-please workflow with proper CI wait and debugging ([7740fd8](https://github.com/motoish/mouse-keepalive/commit/7740fd80dbb02408f0a1ca8f7388e000f47a177d))
* modify mergify setting ([5f2e5a5](https://github.com/motoish/mouse-keepalive/commit/5f2e5a56a3d1084f57492f7b87c8c2652f9abd0c))
* modify pull_request types ([5a00584](https://github.com/motoish/mouse-keepalive/commit/5a00584234dafe36ce39f9ba5682d26a6903a56c))
* modify release-please config file ([88caf44](https://github.com/motoish/mouse-keepalive/commit/88caf44888991648433fccc87981c0c69c305e2c))
* pass secrets as inputs to composite action ([b75f8fa](https://github.com/motoish/mouse-keepalive/commit/b75f8faaea91757126fa709459682fd959d882f6))
* remove trailing spaces and extra blank lines in version-bump.yml ([4a5fc6f](https://github.com/motoish/mouse-keepalive/commit/4a5fc6f21185a95974ffc9a6c4b5c63670e49cc2))
* replace archived repo-sync/pull-request with GitHub CLI ([6adb1d5](https://github.com/motoish/mouse-keepalive/commit/6adb1d54af0f4df123078fbeb624ff595b9da0dd))
* resolve flake8 linting errors ([19c1662](https://github.com/motoish/mouse-keepalive/commit/19c16623ce2d929ce3c28275239a1224619295f9))
* resolve YAML linting errors ([0c5e955](https://github.com/motoish/mouse-keepalive/commit/0c5e9553775b4d7fa813f356bd2dff53eaf78655))
* specify bash shell for Extract version step on Windows ([4e87c26](https://github.com/motoish/mouse-keepalive/commit/4e87c2641ec07e2eb78d589bc1b5fac5746f65de))
* split long lines in YAML workflows to comply with line-length rule ([f14a284](https://github.com/motoish/mouse-keepalive/commit/f14a28420ca17a198a50bc822844b87aecc0d8bb))
* use bash line continuation for Windows PyInstaller command ([053eb82](https://github.com/motoish/mouse-keepalive/commit/053eb82b52bef33c33a5e46b6a86d1f42b24780d))
* use sed to update package.json version instead of npm version ([bf3cd95](https://github.com/motoish/mouse-keepalive/commit/bf3cd957e91ef72e0496f33bbf73903d3f0b7e6b))

## [1.1.0](https://github.com/motoish/mouse-keepalive/compare/mouse-keepalive-v1.0.0...mouse-keepalive-v1.1.0) (2026-01-07)


### Features

* add cross-platform executable builds for GitHub Releases ([d5c4601](https://github.com/motoish/mouse-keepalive/commit/d5c4601ed1283f08a6e49b220744ff5b8e47896a))
* add Makefile to simplify development commands ([39caf65](https://github.com/motoish/mouse-keepalive/commit/39caf654c63cd4c94191b9e447ce5d9f72644f22))
* integrate release-please for automated version management ([559c469](https://github.com/motoish/mouse-keepalive/commit/559c469a5a4df29d0b83e34681d47597fda72615))


### Bug Fixes

* add id-token permission ([375f380](https://github.com/motoish/mouse-keepalive/commit/375f380f9b36b2b841946625c9ccc7df2677e035))
* add mergify and modify README.md ([860bf14](https://github.com/motoish/mouse-keepalive/commit/860bf1477cdc1113edf448aee06f24908cb7d5aa))
* add release-please config-file and manifest-file ([aa59810](https://github.com/motoish/mouse-keepalive/commit/aa598102c708ce277f5d2ccb5e0f74f856577e48))
* improve release-please workflow and fix package name ([f9583bb](https://github.com/motoish/mouse-keepalive/commit/f9583bb0a37a132b3a2914295be236bafdedda2d))
* improve release-please workflow with proper CI wait and debugging ([7740fd8](https://github.com/motoish/mouse-keepalive/commit/7740fd80dbb02408f0a1ca8f7388e000f47a177d))
* modify mergify setting ([5f2e5a5](https://github.com/motoish/mouse-keepalive/commit/5f2e5a56a3d1084f57492f7b87c8c2652f9abd0c))
* modify pull_request types ([5a00584](https://github.com/motoish/mouse-keepalive/commit/5a00584234dafe36ce39f9ba5682d26a6903a56c))
* modify release-please config file ([88caf44](https://github.com/motoish/mouse-keepalive/commit/88caf44888991648433fccc87981c0c69c305e2c))
* pass secrets as inputs to composite action ([b75f8fa](https://github.com/motoish/mouse-keepalive/commit/b75f8faaea91757126fa709459682fd959d882f6))
* remove trailing spaces and extra blank lines in version-bump.yml ([4a5fc6f](https://github.com/motoish/mouse-keepalive/commit/4a5fc6f21185a95974ffc9a6c4b5c63670e49cc2))
* replace archived repo-sync/pull-request with GitHub CLI ([6adb1d5](https://github.com/motoish/mouse-keepalive/commit/6adb1d54af0f4df123078fbeb624ff595b9da0dd))
* resolve flake8 linting errors ([19c1662](https://github.com/motoish/mouse-keepalive/commit/19c16623ce2d929ce3c28275239a1224619295f9))
* resolve YAML linting errors ([0c5e955](https://github.com/motoish/mouse-keepalive/commit/0c5e9553775b4d7fa813f356bd2dff53eaf78655))
* specify bash shell for Extract version step on Windows ([4e87c26](https://github.com/motoish/mouse-keepalive/commit/4e87c2641ec07e2eb78d589bc1b5fac5746f65de))
* split long lines in YAML workflows to comply with line-length rule ([f14a284](https://github.com/motoish/mouse-keepalive/commit/f14a28420ca17a198a50bc822844b87aecc0d8bb))
* use bash line continuation for Windows PyInstaller command ([053eb82](https://github.com/motoish/mouse-keepalive/commit/053eb82b52bef33c33a5e46b6a86d1f42b24780d))
* use sed to update package.json version instead of npm version ([bf3cd95](https://github.com/motoish/mouse-keepalive/commit/bf3cd957e91ef72e0496f33bbf73903d3f0b7e6b))
