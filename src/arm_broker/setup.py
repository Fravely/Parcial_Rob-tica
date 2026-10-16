from setuptools import setup
package_name = 'arm_broker'
setup(name=package_name,version='0.1.0',packages=[package_name],
      data_files=[('share/ament_index/resource_index/packages',['resource/'+package_name]),
                  ('share/'+package_name,['package.xml'])],
      install_requires=['setuptools'],zip_safe=True,
      maintainer='Equipo Robotica',maintainer_email='equipo@ejemplo.invalid',
      description='Broker original con worker unico y metricas RB2',license='Apache-2.0',
      entry_points={'console_scripts':[
          'broker = arm_broker.broker:main',
          'cliente = arm_broker.cliente:main',
          'cliente_sin_laya = arm_broker.cliente_sin_laya:main',
      ]})
