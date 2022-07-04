## Readme
>This is repository for collect data birds view using multiple camera using multithreading.

## How to use?
1. Set up virtual environment
   1. Open using Pycharm
      > If Pycharm show just like this picture please press OK. This is created Virtual Env and install all requirements

      ![](assets/img2.png)
   
   2. If not show figure above please open **Terminal** on your Pycharm and **Type**: 
      
      ```python
      python3 -m venv venv
      source venv/bin/activate
      pip install -r requirements.txt
      ```
2. Change the source of image
![img_3.png](assets/img_3.png)

3. Run Program!
   > Type this command in your Terminal
   ```python
   python3 main.py
   ```
## Save images
### Keyboard input
1. a
   - Save image to images/ directory
   
make sure you save it correctly, because with multithreading 4 image some difficult to interrupt

> Image will same in **images** directory:

   ![img.png](assets/img4.png)

## Record video
Change self.record become True to record
![img_2.png](assets/img_6.png)

> Video will save in **video** directory

   ![img_1.png](assets/img_5.png)

Note:
   1. You can change location of image save by yourself
   2. After save please **move** or **change** the name of the file so overwrite no happens
