# Finding Primes into a File

This program involves severals tasks revolving around prime numbers. You need to write a function that checks whether a number is prime or not, and you need to write code that reads strings from a file. Then, you make use of existing code to convert each string to an integer, using the aforementioned function to check whether the integer is a prime, reversing the integer, and checking whether its reverse is a prime. 

When executing the program, one must give as an argument the name of the file. Three files were provided for you to practice and be tested: `small_file.txt`, `medium_file.txt`, and `large_file.txt`. The program runs with only one file at a time.


## What to Do

1. With your partner, edit the `file_prime.cc` source file using VS Code. Add the required header. Replace all the TODO comments with working code.
1. Your program must use the `IsPrime` function. Do not change the prototype of this function (name, return type, argument types).
1. Compile your program with the `$ make` shell command. Use the **debug compile error** procedure to debug any compile errors.
1. Run your program with the `$ ./file_prime` shell command.
1. Test that your program passes all of the test cases in the test suite above. If your program suffers a runtime error, use the **debug runtime error** procedure to debug the error. If your program does not produce the expected output, use the **debug logic error** procedure to debug the error.
1. Test your program against automated test with the `$ make test` command. Debug any runtime errors or logic errors using the same procedures.
1. Check your header with the `$ make header` shell command. Correct any errors.
1. Check for format errors with the `$ make format` shell command. Correct any errors.
1. Check for lint errors with the `$ make lint` shell command. Correct any errors.
1. After your program passes all of these tests and checks, push your code to GitHub. Use the usual trio of commands: `git add`, `git commit`, and `git push`.

## Checking If a Number is Prime

Given the number 3,137, how can we check to see if it is a [prime number](https://en.wikipedia.org/wiki/Prime_number)?

Remember a prime number is only divisible by 1 and itself. An example of a prime number is the number 2. It can only be divided by 1 and by itself, 2. Another prime number is 13. There are no numbers less than 13 which divide it evenly. On the other hand, a number like 10 is composite. Composite means that you can express the number as the product of two other, smaller, numbers. For instance, 10 can be expressed as 2 * 5.

If we have the number 3,137, we can check every number from 2 until (3,137 - 1) to see if 3,137 can be divided by all those candidate numbers. If we find a number that divides evenly into 3,137 then we know that 3,137 is composite. Otherwise, 3,137 is prime.

The algorithm [Trial Division](https://en.wikipedia.org/wiki/Trial_division), first described by Fibonacci in 1202 CE, is not the best way to discover if a number is prime yet it is easy to program.

All we would have to do is write a `for` loop that starts at 2 and counts up to the number we are interested in. Let's say we want to verify that 23 is prime. Our for loop starts at 2 and counts up to 23, stopping at 22. Every steps of the way, we use the modulo `%` operator to see if 23 modulo the current count has any remainder. If 23 modulo the counter has no remainder then the number is not prime. Otherwise, if we reach the end of the loop without finding any number that evenly divides into 23 then we know 23 is prime.

Can you think of a way to speed this up? Do you really need to check all the numbers for 23?

Let's look at all the number we have to use: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22.

Do we really need to check to see if 23 is divisible by 20? Or by 16? or by 15? Note that 20 is a composite number made up of 4 * 5 or 2 * 10. The number 16 is made up of 2 * 8 or 4 * 4. The number 15 is made up of 3 * 5. Do you see a pattern or relationship?

Originally, we thought our loop would like something like this:

```c++
int input_number = 23;
for(int counter = 2; counter < input_number; counter++){
  // check if prime
}
```

We don't need to count up to `input_number`. In fact we only need to count up to the [square root of `input_number`](https://en.wikipedia.org/wiki/Trial_division#Method). The loop can be rewritten as:

```c++
int input_number = 23;
for(int counter = 2; counter <= IntegerSquareRoot(input_number); counter++){
  // check if prime
}
```

We can make use of the function [sqrt](https://en.cppreference.com/w/cpp/numeric/math/sqrt) to compute the integer square root of the `input_number`.

## Reading From a File

Working with data in the computer's memory is a good starting point. We've done that with a variety of different types (int, float, string). The next challenge for us to over come is how to read and write from [files](https://en.wikipedia.org/wiki/Computer_file).

Reading from files is a great leap forward. Writing programs that can read from a file means that you are no longer limited to what a human can enter at the computer's console. Reading from a file means that you can make use of much more interesting (and larger!) data sources. The smallest and most portable computer can store Gigabytes of data. That is a lot of space to store files (and database)!

How big of a file can your fit on your computer? Is there a limit to how large or how many files you can have on your computer? How big is the smallest file?

A file is just an abstraction of some information that is stored in your computer's [file system](https://en.wikipedia.org/wiki/File_system). It's an address of sorts to help you, the programmer, locate a resource that has been stored in your computer's file system.

You can think of a path to a file kind of like a [URL](https://en.wikipedia.org/wiki/URL) to a website. If you have the right path, your computer can open up the file and read it. (And if you think about it a little bit you may ask yourself if you can read from a file, then how hard can it be to read from a website?).

The first thing we need is an abstraction of what a file is. For the programmer, a file is a stream. A stream not in the sense of a flowing body of water but a sequence that streams by. More like a train which has a beginning, middle, and end. Given a stream in C++, we want to have operations to read from it and move forward and backwards.

For starters, let's focus on opening up a file and reading string by string from it. C++ has a special type called [`ifstream`](https://en.cppreference.com/w/cpp/io/basic_ifstream) which is defined in the `fstream` header file. If we have the name of a file such as `"file_with_numbers.txt"`, then we can open and manipulate the file with the following code:

```c++
std::string file_name{"file_with_numbers.txt"};
std::ifstream input_file_stream(file_name);
```

The variable `input_file_stream` is of type `ifstream` or input file stream. It is a C++ object which is allocated and initialized with the file path `"file_with_numbers.txt"`. From here, we can perform operations such as checking to see if the file was successfully opened or read a line of text from the file.

To read a string from a input file stream one will use the `>>` operator, as reading from `std::cin`.

Our strategy is to first declare a `std::string` variable and then use `input_file_stream >>` to copy the string from the file stream into the temporary variable. Let's assume the variable `input_file_stream` successfully opened `"file_with_numbers.txt"` and the first string in the file is "17831".

```c++
std::string file_name{"file_with_numbers.txt"};
std::ifstream input_file_stream(file_name);
std::string some_string;
input_file_stream >> some_string;
std::cout << some_string << "\n";
input_file_stream.close();
```

On the last line, `input_file_stream` is closed because we are no longer using it. If you open something, like a file, you must close it. Not closing a file leaves it locked and perhaps in an undefined state.

In the example above, we assumed the file existed and was opened without a problem. This is not a good practice. Whenever opening a file, always check to make sure the file was opened. This short and simple check ensures that the file is open and ready to be read from.

```c++
std::string file_name{"words_that_start_with_m.txt"};
std::ifstream input_file_stream{file_name};
if (!input_file_stream.is_open()) {
    std::cout << "Could not open the file " << file_name << ". Exiting.\n";
    return 1;
}
std::string some_string;
input_file_stream >> some_string;
std::cout << some_string << "\n";
input_file_stream.close();
```

We only read one line of text in the given example. What if we want to read the contents of an entire file? Consider that a file is composed of many lines of text.

To read the contents of an entire file, all one needs to do is to use `input_file_stream >>` in a loop.

For example, to read all the lines in a file using a while loop:
```c++
std::string file_name{"words_that_start_with_m.txt"};
std::ifstream input_file_stream{filename};
while (input_file_stream.good()) {
	std::string some_string;
    input_file_stream >> some_string;
}
input_file_stream.close();
```

Finally, if we want to know if we have been successful in reading to the end of the file, we can ask the `std::ifstream` what's happened. You can only check the status of an `std::ifstream` while it is open. You cannot check its status after you have closed it. The following if-else-if block can be used right before the `std::ifstream` is closed to print its status to the terminal.

```c++
if (input_file_stream.eof()) {
  std::cout << "End of file reached successfully!\n";
} else if (input_file_stream.bad()) {
  std::cout << "I/O error while reading.\n";
  return 1;
} else if (input_file_stream.fail()) {
  std::cout << "Failure: Long line.\n";
  return 1;
}
input_file_stream.close();
```

We typically do not print a message when we successfully reach the end of a file like in the example above. In your program, you may want to print out a message like this to help yourself understand how your program works. When you've finished with your lab, make sure to comment out any extra messages that don't meet the exercise's requirements.

Once we read a string, we need to check that is not the empty string `""`, then convert it to an integer using [stoi](https://en.cppreference.com/w/cpp/string/basic_string/stol) function, then check whether the integer is a prime or not.

## Reversing a string

How do we reverse a string? There are many ways to do this. The best approach is to use the tools available in the C++ standard library.

There is a concept in programming called an [iterator](https://en.wikipedia.org/wiki/Iterator). It's a tool that allows a programmer to move forwards or backwards through a container or sequence like a string. Usually, we want to start at the beginning and move (or iterate) to the end. For `std::string`, there are the member functions [begin()](https://en.cppreference.com/w/cpp/string/basic_string/begin) and [end()](https://en.cppreference.com/w/cpp/string/basic_string/end).

To reverse a string, do we move from the beginning to the end? Consider the string "12053". The reverse of "12053" is "35021". Did you move from the beginning to the end to reverse "12053"? More than likely, you reversed "12053" by moving from the end to the beginning. In C++, there are member functions which return reverse iterators [rbegin()](https://en.cppreference.com/w/cpp/string/basic_string/rbegin) and [rend()](https://en.cppreference.com/w/cpp/string/basic_string/rend).

An example of how to reverse a string in C++ is the following:
```c++
std::string favorite_number{"12053"};
std::string reversed_favorite_number{favorite_number.rbegin(), favorite_number.rend()};
// This will print "35021"
std::cout << reversed_favorite_number << "\n";
```

The reverse iterators are used to initialize `reversed_favorite_number` with the letters from `favorite_number` in reverse order.

Once we have the reverse number, since it is a string, we need to convert it to an integer using `stoi` function.

## Next Steps

After you have pushed your code, move on to part 2.
