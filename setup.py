from setuptools import setup, find_packages

setup(name='gym_pikachu_volleyball',
      version='0.0.1',
      install_requirements=['gym'],
      packages=find_packages(),
      package_data = {'sprites': ['envs/sprites/*']},
      zip_safe = False
)

