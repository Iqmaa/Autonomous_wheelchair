from setuptools import find_packages, setup

package_name = 'wheelchair_script'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='iqma',
    maintainer_email='105384156+Iqmaa@users.noreply.github.com',
    description='obstcle avoidance and behaviour logic',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'obstacle_avoidance = wheelchair_script.obstacle_avoidance:main',
        ],
    },
)
