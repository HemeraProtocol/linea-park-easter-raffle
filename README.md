# Linea Park Easter Raffle

## How it works

### Task Master Prize

Random LXP drop within the range of [150] LXP to [250] LXP for Linea park participants that completing 60% of all Basic Tasks in Linea, PoH Completion.
Check https://layer3.xyz/quests/easter-surprise-1 for more information
LXP allocation through raffle:

- 150 LXP: 55% of participants
- 200 LXP: 25% of participants
- 225 LXP: 15% of participants
- 250 LXP: 5% of participants

The script will randomly shuffle the list based on a seed phrase. The first 55% wallets win 150 LXP, next 25% wallets win 200 LXP, next 15% win 225 LXP and last 5% win 250 LXP.

### Jackpot Bonus Prize

Eligibility: 70% of all Bonus Tasks in Linea, PoH Completion.
Check https://layer3.xyz/quests/easter-surprise-2 for more information.
Projects all together contribute two categories of prize: one that all eligible participants will get, the other are fixed amount of prized for the raffle.
The script will randomly shuffle the list based on a seed phrase. Then distribute the fixed number prize in the same order as it's listed in the csv file.
One wallet will get at most one of the fixed amount prize.

## Raffel Result

### Input File

| File name                                | MD5                              |
| ---------------------------------------- | -------------------------------- |
| linea_park_easter_raffle.py              | dfb5ee44375815f5986db32b19078779 |
| task_master_prize_eligible_wallets.csv   | 1050849c33db4c3fbcfdc5954f9b1920 |
| jackpot_bonus_prize_eligible_wallets.csv | 203175c053736e7f679a3d958e550607 |
| jackpot_bonus_prize.csv                  | 45f9107e59f41804ec6188f97c8aede4 |

### Seed Phrase

"linea" for the task master pool
"build" for the jackpot bonus pool

### Run Script

```
python3 linea_park_easter_raffle.py linea build
INFO:root:Start to run task master prize pool
INFO:root:Read 776391 wallet addresses
INFO:root:Clean up wallet addresses
INFO:root:After clean up, there are 776391 wallet addresses
INFO:root:Ordering wallet addreses based on seed phrase '5'
mINFO:root:Starting to assign prize based on the wallet list order
INFO:root:Complete! Now output the task master prize results..
INFO:root:Start to run task master prize pool
INFO:root:Read 214038 wallet addresses
INFO:root:Read 5 prizes from the jackpot pool
INFO:root:Clean up wallet addresses
INFO:root:After clean up, there are 214038 wallet addresses
INFO:root:Ordering wallet addreses based on seed phrase '5'
INFO:root:Starting to assign prize based on the wallet list order
INFO:root:Complete! Now output the jackpot bonus prize results..
```

### Expected Outputs

You should be able to run the script on your own and it should generate exactly the same output with the same seed phrase

| File name                       | MD5                              |
| ------------------------------- | -------------------------------- |
| task_master_prize_results.csv   | b5ae84827627b7912506847046d07faf |
| jackpot_bonus_prize_results.csv | 90cb2e6399d6fd5f57e3b06b505adc4e |
