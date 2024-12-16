# Password Cracking Simulation
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
  <img src="https://i.imgur.com/ECOh7dt.gif" height="10%" width="55%" alt="Disk Sanitization Steps"/> <br/>
  This password was three digits which is very short, so the program took only a few seconds to crack the password. However, the longer the password, the longer it takes to crack.  This demonstration emphasizes the importance of password length.
</p>

<h3>Dictionary Attack Password Crack Simulator:</h3>
The user provides a hashed password and a file containing a list of candidate passwords (dictionary).
The program hashes each word in the dictionary using the MD5 hashing algorithm and compares it to the given hash.
The attack demonstrates how easily simple, common passwords can be cracked using pre-existing wordlists.

<h4 align="center">Example Usage:</h4>
<p align="center">
  <pre>
  <code>
Enter the hashed password: 098f6bcd4621d373cade4e832627b4f6
Enter password filename including path: wordlist.txt
Password found: test
  </code>
  </pre>
</p>
<h4 align="center">Demo:</h4>
<p align="center">
  Here, I used a <a href="https://www.md5hashgenerator.com/" target="_blank">MD5 Hash Generator</a> to hash the password “sunshine” and input it as user prompt, then... <br/>
  <img src="https://imgur.com/eJNJVB6.gif" height="80%" width="80%" alt="Disk Sanitization Steps"/> <br/>
  The password was cracked in an instant by entering the file (dictionary) where the password candidates are stored. This is much faster than Brute Force Attack
</p>

<h2>Conclusion:</h2>
This project demonstrates the differences in efficiency between brute force and dictionary attacks. Brute force attacks, while exhaustive, are computationally expensive and impractical for complex passwords. In contrast, dictionary attacks leverage precompiled wordlists, making them much faster for cracking simple or common passwords.
However, this project also highlights a critical limitation of using outdated hashing algorithms like MD5. Even though the passwords were hashed, the dictionary attack successfully cracked them by matching precomputed hash values. This underscores the importance of not only using strong, unique passwords but also employing modern, secure hashing algorithms like bcrypt or Argon2, which are designed to resist such attacks.
 

<!--
 ```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```
--!>
