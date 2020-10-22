from setuptools import find_packages, setup

with open("requirements.txt") as f:
    install_requirements = f.read().splitlines()

with open("requirements-dev.txt") as f:
    test_requirements = f.read().splitlines()

setup(
    name="wallet_api",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=install_requirements,
    tests_require=test_requirements,
    setup_requires=["pytest-runner"],
    test_suite="tests",
)
