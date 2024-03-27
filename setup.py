from distutils.core import setup

setup(
    name="cellcv",
    version="0.0",
    author="jendralhxr, m172205, d191761",
    packages=["cellcv"],
    url="https://github.com/jendralhxr/uget2",
    license="MIT License",
    author_email="zulhaj@hiroshima-u.ac.jp",
    description="Cell counting and motility evaluation estimation on from video data",
    python_requires=">=3.7",
    install_requires=[
        "opencv-python>=4.6",
        "numpy>=1.15",
        "matplotlib>=3.4",
    ],
)
