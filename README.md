# ThatOneGuysPotionMaker
Creates every potion is osrs using Kelltoms OSBC

Import this into your /src/model/osrs folder
add from .PotionMaker.Potion_Maker import OSRSPotionMaker to your "__init__.py" script located in /src/model/osrs

You do not need to move the images. The bot will pull them from it's own folder!

Select your potion and Set your anti-bans

YOU MUST SELECT A MOUSE SPEED other anti-bans are optional. 

![image](https://user-images.githubusercontent.com/125089137/218597555-fce7e4b9-e829-4ecf-bb00-42695ed8962e.png)
![image](https://user-images.githubusercontent.com/125089137/218599234-86f60e7b-1c60-4450-ac08-336f510b4389.png)



Ensure your brightness setting is set to the middle. 

![image](https://user-images.githubusercontent.com/125089137/218599062-de3e0d80-e80a-4319-9e8a-1603dcac447c.png)



Stand near a Bank marked using cyan

![image](https://user-images.githubusercontent.com/125089137/218598211-46a89db8-1e59-4a99-9b27-d047eccce752.png)


You must have a bank tab with an empty vial as an icon. To do this put an empty vial as the first item. This is where you will put your potion making
supplies. I reccomend only putting the supplies you are currently making in this tab. Image recognition is not 100% and will sometimes confuse similar herbs
I tried to rememdy this as best as possible but it still happens. For instance in the following picture Guam and Marrentill will confuse the bot. OCR could 
not be used because the mouseover text goes over the top of the bank item amount. 

![image](https://user-images.githubusercontent.com/125089137/218598950-46e23c2c-9247-46c5-a6fa-cdc96b587c06.png)

If your making a potion that requires a stackable ingrediant like stamina,divine,ancient brew, etc... Make a single potion first and withdrawl your stackable item
into your inventory. Depoit the potion and set bank fillers to all. This will ensure that your stackable's will not be redeposited into the bank.

![image](https://user-images.githubusercontent.com/125089137/218599929-301c5924-cff8-4190-8499-961560234f54.png)
