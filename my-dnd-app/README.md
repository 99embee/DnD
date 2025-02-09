# my-dnd-app/my-dnd-app/README.md

# My C++ Application

This is a simple C++ application that outputs a message to the console.

## Project Structure

```
my-dnd-app
├── src
│   └── main.cpp        # Entry point of the application
├── CMakeLists.txt      # CMake configuration file
└── README.md           # Documentation for the project
```

## Building the Application

To build the application, follow these steps:

1. Ensure you have CMake installed on your system.
2. Open a terminal and navigate to the project directory.
3. Create a build directory:
   ```
   mkdir build
   cd build
   ```
4. Run CMake to configure the project:
   ```
   cmake ..
   ```
5. Build the application:
   ```
   make
   ```

## Running the Application

After building the application, you can run it with the following command:

```
./my-dnd-app
```

You should see the output:

```
Hello, World!
```