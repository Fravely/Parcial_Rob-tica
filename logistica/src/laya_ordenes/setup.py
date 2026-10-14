from setuptools import find_packages, setup

package_name = 'laya_ordenes'
setup(
    name=package_name,
    version='0.2.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Equipo Robotica',
    maintainer_email='equipo@example.org',
    description='Interprete de ordenes LAYA HTTP, interfaz web y transcriptor de voz',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'interprete_ordenes = laya_ordenes.node:main',
            'orden_a_broker = laya_ordenes.orden_a_broker:main',
            'orden_a_recogida = laya_ordenes.orden_a_recogida:main',
            'interfaz_ordenes = laya_ordenes.interfaz_ordenes:main',
            'transcriptor_voz = laya_ordenes.transcriptor_voz:main',
        ],
    },
)
