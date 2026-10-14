from setuptools import setup, find_packages

setup(
    name='weather_wizard',
    version='0.1.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "opencv-python",
        "mediapipe",
        "numpy",
    ],
    entry_points={
        "console_scripts" : [
            "weather-wizard=weather_wizard.main:main",
        ],
    },
    python_requires=">=3.12",
)