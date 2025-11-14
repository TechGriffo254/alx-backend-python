#!/usr/bin/env python3

TEST_PAYLOAD = [
  (
    {"repos_url": "https://api.github.com/orgs/google/repos"},
    [
      {
        "id": 7697149,
        "name": "episodes.dart",
        "license": {
          "key": "bsd-3-clause",
          "name": "BSD 3-Clause \"New\" or \"Revised\" License",
          "spdx_id": "BSD-3-Clause",
          "url": "https://api.github.com/licenses/bsd-3-clause",
          "node_id": "MDc6TGljZW5zZTU="
        }
      },
      {
        "id": 7776515,
        "name": "cpp-netlib",
        "license": {
          "key": "bsl-1.0",
          "name": "Boost Software License 1.0",
          "spdx_id": "BSL-1.0",
          "url": "https://api.github.com/licenses/bsl-1.0",
          "node_id": "MDc6TGljZW5zZTI4"
        }
      },
      {
        "id": 7968417,
        "name": "dagger",
        "license": {
          "key": "apache-2.0",
          "name": "Apache License 2.0",
          "spdx_id": "Apache-2.0",
          "url": "https://api.github.com/licenses/apache-2.0",
          "node_id": "MDc6TGljZW5zZTI="
        }
      },
      {
        "id": 8165161,
        "name": "ios-webkit-debug-proxy",
        "license": {
          "key": "other",
          "name": "Other",
          "spdx_id": "NOASSERTION",
          "url": None,
          "node_id": "MDc6TGljZW5zZTA="
        }
      },
      {
        "id": 8459994,
        "name": "google.github.io",
        "license": None
      },
      {
        "id": 8566972,
        "name": "kratu",
        "license": {
          "key": "apache-2.0",
          "name": "Apache License 2.0",
          "spdx_id": "Apache-2.0",
          "url": "https://api.github.com/licenses/apache-2.0",
          "node_id": "MDc6TGljZW5zZTI="
        }
      },
      {
        "id": 8858648,
        "name": "build-debian-cloud",
        "license": {
          "key": "other",
          "name": "Other",
          "spdx_id": "NOASSERTION",
          "url": None,
          "node_id": "MDc6TGljZW5zZTA="
        }
      },
      {
        "id": 9060347,
        "name": "traceur-compiler",
        "license": {
          "key": "apache-2.0",
          "name": "Apache License 2.0",
          "spdx_id": "Apache-2.0",
          "url": "https://api.github.com/licenses/apache-2.0",
          "node_id": "MDc6TGljZW5zZTI="
        }
      },
      {
        "id": 9065917,
        "name": "firmata.py",
        "license": {
          "key": "apache-2.0",
          "name": "Apache License 2.0",
          "spdx_id": "Apache-2.0",
          "url": "https://api.github.com/licenses/apache-2.0",
          "node_id": "MDc6TGljZW5zZTI="
        }
      }
    ],
    ['episodes.dart', 'cpp-netlib', 'dagger', 'ios-webkit-debug-proxy', 'google.github.io', 'kratu', 'build-debian-cloud', 'traceur-compiler', 'firmata.py'],
    ['dagger', 'kratu', 'traceur-compiler', 'firmata.py'],
  )
]
