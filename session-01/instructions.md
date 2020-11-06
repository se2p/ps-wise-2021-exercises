# Programming Styles -- WiSe 20-21
--------

# Setup and Installation
Set up and install the environments necessary for the exercises and the assignments in this course. 
We will use three different programming languages to implement the different styles: Python (3.7) for the exercises; Java (JDK 11) and JavaScript (NodeJS v10.23) for the assignments and some exercises. 

## Install Python 3.7
- Creating the Python environment using Anaconda would be a good option in order to isolate different version of python on your local machine.
### Install Python3 (for Mac)
Those instructions assume that either you have or are willing to install XCode and Home Brew (see [https://programwithus.com/learn-to-code/install-python3-mac/](https://programwithus.com/learn-to-code/install-python3-mac/)). If you prefer to install python3 manually, check: [https://www.saintlad.com/install-python-3-on-mac/](https://www.saintlad.com/install-python-3-on-mac/)

#### 1. Install Xcode
Xcode is Apple's Integrated Development Environment (IDE). You might already have Xcode on your Mac. If not, you can get Xcode from the Apple store.

#### 2. Install Brew
Homebrew installs the stuff you need. Homebrew is a package manager for Mac OS

1. Launch Terminal
2. Install HomeBrew:
```/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"```

#### 3. Install Python3 with Brew
1. Launch Terminal
2. Run:
```brew install python3```

Check the output of this command: 
```python3 --version```

#### 4. Optionally Install PyEnv

If you need to install multiple versions of python, I suggest you to use PyEnv. You can read more about PyEnv at [https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)

Also PyEnv can be installed using Brew:
```brew install pyenv```

> TODO: If you know other ways to manage different versions of Python let us know!

### Install Python3.7 (for Window)
The following instructions were taken from:
[https://realpython.com/installing-python/#step-1-download-the-python-3-installer](https://realpython.com/installing-python/#step-1-download-the-python-3-installer)

#### 1. Download the Python 3 installer
Go to the download page for Windows at python.org and choose either the 32-bit or 64-bit installer. If your system has a 32-bit processor, then you should choose the 32-bit installer, otherwise go with the 64-bit system.

#### 2. Run the Installer
Once you have chosen and downloaded an installer, simply run it by double-clicking on the downloaded file and check the box that says **Add Python 3.x to PATH** to ensure that the interpreter will be placed in your execution path.

> TODO: If you know other ways to install and manage different versions of Python let us know!

### Install Python3.7 (for Linux)
First of all, try to update the repositories and also install `software-properties-common` package using the following command:
```
sudo apt-get update
sudo apt-get install software-properties-common
```
The following command should work:
```
sudo apt-get install python3.7
```
But in case you encounter an error, you should add `deadsnakes` repository and try again:
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.7
```

> TODO: Probably you can use pyEnv also under Linux, but I never tried that.
If you know other ways to install and manage different versions of Python let us know!


## Install Java 11

### 1.Install JDK From Oracle
If you do not already have a Java JDK on your system, please install it from [Oracle's Java site](https://docs.oracle.com/en/java/javase/11/install/installation-jdk-microsoft-windows-platforms.html#GUID-A7E27B90-A28D-4237-9383-A58B416071CA). 

We will use **Java 11** in this course.
Note you must install the JDK (The Java Development Kit), which includes a JVM and the tools a developer needs (e.g., javac, the Java compiler).

If you do not like to use Oracle's JDK you might want to use other implementations (e.g., OpenJDK)

Check that you have the right version using:
```java -version```

### 2.Install JDK using Brew/Cask
According to this [link](https://medium.com/macoclock/using-homebrew-to-install-java-jdk11-on-macos-44b30f497b38) you can install java 11 also as follows:

Update HomeBrew and add the casks tap of HomeBrew.

```
$ brew update
$ brew tap homebrew/cask-versions
```

Install Version 11 of Java JDK.

```
$ brew cask install java11
$ java --version
```

### 3. Optionally Install jEnv
jEnv is a little utility similar to pyEnv. You can read more about jEnv [here](https://www.jenv.be/). I suggest you to install jEnv to easily manage multiple Java installations.

jEnv can be also installed using Brew:
```brew install jenv```


### 4. Optionally Install SDKMAN!
[SDKMAN!](https://sdkman.io/) is another alternative for managing multiple JDK installations, similar to jEnv.

SDKMAN! installs smoothly on Mac OSX, Linux, WLS, Cygwin, Solaris, FreeBSD, and you can also easily install it on your Windows machine through [Git for Windows BASH](https://git-scm.com/download/win).

>TODO: For Linux Java can be installed using the available package manager (e.g., `apt-get`). For Windows, I suspect that the most viable option is to download the installer from Oracle's Web page. In any case,  feel free to contribute additional ways to install Java and utilities to handle multiple Java versions

## Install NodeJs 

### Install NodeJs (Mac Os)
We use Node.js v10.23 as the JavaScript environment in this course. 

You're free to install it in whatever way you want, but I suggest to use `nvm` (Node Version Manager). `nvm` can be used also to manage multiple versions of node on the same machine. 

You can install `nvm` using Homebrew:

```
brew install nvm
```

Once you have nvm, you can install the version of node that you need:

```
nvm install 10.23
```

Before you can start using this version of node you need to enable it

 ```
 nvm use 10.23
 ``` 


Check which version of node you are using:

```
node --version
```

### Install NodeJs (Windows)
There are two possible ways for installing  NodeJS under Windows.

#### 1. Install NodeJs using the official installer
You can find [this page](https://nodejs.org/en/download/) to download and use the official installer. For installing version 10.23, you can use [this link](https://nodejs.org/dist/latest-v10.x/). There you can choose `node-v10.23.0-x64.msi` in case your Windows machine is 64-bit.

#### 2. Install NodeJs using Chocolatey package manager
[Chocolatey](https://chocolatey.org/) is a package manager for Windows. You can install it via PowerShell. You can find the installation instruction [here](https://chocolatey.org/install).
If you have already installed Chocolatey, then you can easily use the following command:

```
choco install nodejs --version=10.23
```

Please note that you need to run the PowerShell as administrator to install it. After that, `node` is accessible through any other Terminal.

#### Install NodeJs (Linux)
> TODO Those instructions are missing... maybe you can add them?

### Install an IDE
You are free to use any IDE for programming. Common choices are:

- Eclipse or IntelliJ for developing in Java (I will use Eclipse)
- PyCharm for developing in Python
- Visual Studio Code (not VisualStudio!) as JavaScript editor

> NOTE: when possible select an IDE that makes it possible to DEBUG your code !
