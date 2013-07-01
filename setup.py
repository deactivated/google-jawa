from setuptools import setup

setup(name="google-jawa",
      version="0.1",
      long_description="",
      scripts=["bin/google-jawa"],
      packages=["google_jawa"],
      install_requires=['libgreader'],
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          "Development Status :: 4 - Beta",
          "License :: OSI Approved :: MIT License",
          "Intended Audience :: Developers",
          "Natural Language :: English",
          "Programming Language :: Python"])
