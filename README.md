# genv
Quickly environment setting. 

Sometimes there are too many settings I need to remember. 
I think I should have a better way to handle them.
I will keep update it, until it is good enough to cover my cases.

# How to install

* Clone the repository into local disk

```commandline
git clone https://github.com/GilbertHuang84/genv.git
```

* In windows, you should set the system *path* to the {clone folder}/src.

* I did not support Linux, because my machine is windows. If anyone wants to contribute is welcome.

# How to use

I have my settings saved in the project, I will remove it in the future.

```commandline
# init the usd environment
init usd

# init the dev environment
init dev

# init the python2 environment
init py2
```

You can also call it in python. But it is not stable now, it will be failed in some cases.
I will fix in the future.

```python
import settings

# init the usd environment
settings.to_env('usd')


# init the dev environment
settings.to_env('dev')

# init the python2 environment
settings.to_env('py2')

```

# Where is the settings

The settings file is under {clone folder}/src/settings/env_settings.json.

# Contact me

My email: [laobo_huang@163.com](mailto:laobo_huang@163.com)


