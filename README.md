# Dice2Seed

## This version of the tool has been edited to work in the AnuBitux operating system. To use it in other environments, refer to the [main branch](https://github.com/ASeriousMister/Dice2Seed)

This tool creates BIP39 mnemonic seeds from entropy obtained rolling a dice a lot of times.
To see how it works, you can also refer to this [tutorial](https://anubitux.org/how-to-generate-a-mnemonic-seed-with-anubitux-and-a-dice/).

### Installation
Install git, python3 and pip (if needed):
```
sudo apt install git python3 python3-pip
```
Clone the repository:
```
git clone https://github.com/ASeriousMister/Dice2Seed
```
Move to the tool's directory
```
cd /path/Dice2Seed
```

### Utilization
User simply has to provide answers to the prompted questions.
At the end the tool will show the obtained BIP39 mnemonic seed.

Entropy can be obtained tracking dice rolls with the help of the tool or can be pasted as a result of dice rolls or as a sequece of 0s and 1s.

### Example keys
- Dice rolls reuslts (256): 1423353625241324352413243526252525243534666554653645463535262525162525363532526251252626353433533536225356225251414255336355242142253633534242411252535364453534242525161525343422525161625253434252516162525434352521661252443434252516162525434352525166542512
- Binary key: 0000001100101011100101110101101000101000011001011010000111010100000011101100011111110010001000101010010010101101111100010011100111011100110110101001111001110110100011001010100110101101010000010100110000110011011010111101001110010101110010010001000001101001

These keys can be used only to test the tool. Do not send transactions to the addresses generated from the example keys.

### Disclaimer
This ool comes with no guarantees. Do your own research about how this tool works and in general about how cryptocurrency keys work before using it.

### Credits & Donations
This tool is part of the [AnuBitux](https://anubitux.org) project. 
If you appreciate this work visit https://anubitux.org and consider making a donation
- BTC: 1AnUbiYpuFsGrc1JFxFCh5K9tXFd1BXPg
- XMR: 87PTU58siKNb3WWXcP4Hq4CmCb7kMQUsEiUWFT7SvvMMUqVw9XXFGrJZqmnGvuJLGtLoRuEqovTG4SWqkPr8YLopTSxZkkL
