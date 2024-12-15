# Password Cracker Simulation
<h2>Description</h2>
This project consists of two Python scripts that simulate password-cracking techniques: <b>Brute Force Attack</b> and <b>Dictionary Attack</b>. The purpose of the project is to demonstrate the vulnerabilities of short, simple, and common passwords, as well as highlight the importance of secure hashing algorithms.
<br />


<h2>Languages and Utilities Used</h2>

- Python


<h2>Environments Used </h2>

- macOS Sequoia 15.2

<h2>Program walk-through:</h2>
<h3>Brute Force Attack Password Crack Simulator:</h3>
The program prompts the user to input a password.
It generates random combinations of characters until the correct password is found.
This approach shows how inefficient brute force methods are against complex passwords.

<h4 align="center">Example Usage:</h4>

<p align="center">
  <pre>
  <code>
Enter a password (letters, numbers, and symbols only): Pass@123
<==== Abc!xZ ====>
<==== Pass@123 ====>
The Password is: Pass@123
  </code>
  </pre>
</p>

<h4 align="center">Demo:</h4>
<p align="center">
  Here, suppose I entered 3-digit password "jh6" as my user input, then... <br/>
  <img src="https://i.imgur.com/ECOh7dt.gif" height="0%" width="45%" alt="Disk Sanitization Steps"/> <br/>
  Note it only took a few senconds to crack the password.
</p>




<h3>Dictionary Attack Password Crack Simulator:</h3>
The user provides a hashed password and a file containing a list of candidate passwords (dictionary).
The program hashes each word in the dictionary using the MD5 hashing algorithm and compares it to the given hash.
The attack demonstrates how easily simple, common passwords can be cracked using pre-existing wordlists.



<!--
 ```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```
--!>
