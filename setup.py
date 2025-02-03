import setuptools
from setuptools import find_packages
import re

with open("./src/selective_editor/__init__.py", "r") as f:
    content = f.read()
    # from https://www.py4u.net/discuss/139845
    version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', content).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [
        req for req in f.read().splitlines() if req and not req.startswith("#")
    ]

setuptools.setup(
    name="selective_editor",
    version=version,
    author="zuppif",
    author_email="francesco.zuppichini@gmail.com",
    description="<INSERT_DESCRIPTION>",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=requirements,
    extras_require={
        "dev": ["pytest"],
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
