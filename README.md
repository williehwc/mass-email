# Mass Email
A script for sending mass emails over SMTP using [sendEmail](http://caspian.dotconf.net/menu/Software/SendEmail/). Tested on Ubuntu 14.04 and macOS Sierra.

## How to use
Clone this repo, then run `sudo apt-get install sendemail` on Ubuntu or `brew install sendemail` on macOS* to install [sendEmail](http://caspian.dotconf.net/menu/Software/SendEmail/).

*To install Homebrew on macOS, please refer to the instructions at [brew.sh](https://brew.sh).

Next, modify the `config.json` file as follows:

- `server`: the SMTP server, such as `smtp.cs.toronto.edu` or `smtp.office365.com`.
- `port`: the SMTP port number, such as `587`.
- `tls`: use TLS? Choices are `yes`, `no`, and `auto`.
- `from`: the email address from which you are sending the email; either `john@example.com` or `John Smith <john@example.com>` format is accepted. Note that many email servers will intervene (e.g. overwrite your `from` address) if you enter an unauthorized `from` address.
- `username`: your SMTP username; we'll ask for your password later.
- `cc`: an array of email addresses to carbon-copy in every email.
- `bcc`: an array of email addresses to blind carbon-copy in every email.

You'll need a `list.csv` file that defines the email addresses (`to`) and custom variables/fields. For each recipient, you can define a `filename` to use for the email subject and body. If `filename` is not defined, `email.txt` is used. The header row `to,filename,...` is required.

The email file defined by `filename` (or the default `email.txt`) should have at least two lines. The first line will always be the subject. The second line onwards is the body text. In both the subject and the body, fields/variables can be defined using braces. For example, `{name}` in the subject and/or body will be replaced with the `name` defined in `list.csv`.

Finally, run `python3 mass-email.py` (`python` 2.7 should also work); you will be prompted for your SMTP password.