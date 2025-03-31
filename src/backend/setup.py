from setuptools import setup, find_packages

setup(
    name="movie_recommendation_backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        req.strip() for req in open("requirements.txt").readlines() if req.strip()
    ],
    description="Backend for movie recommendation system",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9"
)
