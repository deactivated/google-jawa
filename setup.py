from setuptools import setup

setup(name="google-jawa",
      version="0.1",
      long_description="",
      scripts=["bin/google-jawa"],
      packages=["google_jawa"],
      install_requires=['libgreader'],
      include_package_data=True,
      zip_safe=False)
