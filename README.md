# daikinitm

Daikin ITM is a python library for controlling the Daikin Air-Conditioner.

## Usage




```bash
# You must know the ITM address for each Air-Con unit.

import daikinitm
import time
Host = "192.168.217.60"
Port = 5000
Authorization =  "aXRtoMl0bTEyMzQNjc40TAxMg=="

# Authorization is the Basic Authentication Header Generator.
# Authorization=b64encode(f"{User}:{Password}".encode('utf-8')).decode("ascii")
# or 
# Authorization : https://datafetcher.com/basic-authentication-header-generator
# {User} and {Password} were set in ITM Controller

#initial
Factory1 = daikinitm.itm(Host,Port,Authorization)

# SET FAN 
# Fun  "P" (Power) :  0:Off 1:On
Address = 183
Fun = "P"
Val = 0
print("Before:",Factory1.Status(Address))
print(Factory1.Set(Address,Fun,Val))
time.sleep(5)
print("After:",Factory1.Status(Address))

# SET AIR
# Fun  "P" (Power)              :  0:Off  1:On
# Fun  "T" (Temperature)        :  18,19,20,....,32
# Fun  "M" (Mode)               :  0:Fan 4:Cool 16:Dependent Dry:64
# Fun  "F" (Fan)                :  0:Low 4:Medium 2:High  100:Auto
# Fun  "S" (Air Flow Direction) :  0,1,2,3,4,  7(Swing)

Address = 101
Fun = "T"
Val = 25
print("Before:",Factory1.Status(Address))
print(Factory1.Set(Address,Fun,Val))
time.sleep(5)
print("After:",Factory1.Status(Address))

# Status
# Fan = IP,Port,Address,Products,Power
# Air = IP,Port,Address,Products,Power,Mode,Temp,Room Temp,Fan,Air Flow Direction
