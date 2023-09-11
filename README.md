<h1 align="center">✨ Aria ✨</h1>
<p align="center">An AI personal assistant I designed to make my life easier.</p>

## About Aria

### What can she do?

### Chatting to Aria

## Getting Started

### Dependencies

Before running Aria, make sure all the necessary dependencies are installed. 
This can be done with the _install.py_ script.

```bash
# python can be used in place of python3 in some cases
python3 install.py      
```

**Take Note:** One of the dependencies is a NLP text-similarity module which needs about 600mb to install.

### Potential Issues

#### The playsound Module

Some new versions of the playsound module are not compatible with Aria's text-to-speech module. 
A the *requirements.txt* has a compatible version, but if your device already has playsound installed, the compatible installation may be skipped. 
The issue can be fixed in two ways: </br></br>

- **Option 1: Changing your playsound version**
  You can change your current python environment's playsound version with the following code:

  ```bash
  pip uninstall playsound
  pip install playsound==1.2.2
  ```

- **Option 2: Running Aria inside a virtual environment**
  Option 1 could affect any modules or files on your device which depend on the playsound module.
  If you don't want these files to be affected, you could rather make use of a virtual environment. </br>
  - First <a href="https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/">setup a virtual environment</a>. </br>
  - Once that's done, run the install script from within the environment.

## Plans for Aria

### On the way:

### Ideas:
