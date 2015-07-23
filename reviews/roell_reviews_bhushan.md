There wasn't much in the file that I got from Sinan, I checked your github page for a different .py file, but I didn't find one that contained the sections that Jason referenced in his review.
    - Note: thanks for the updated python script.
    - I couldn't get the script to run, so I was not able to see any of the outputs

#General
* Commenting code inline and by section would make it more understandable for review
* Your concept of analysis comes through well, listing how each step ties to the goal will help make it easier to follow 

###Analysis
* You showed me the graph of stock price by time since an attack during office hours. This was a really interesting graph that could be expanded to show more of what you're after.
    - I think changing the x axis to show change in price would give you a better reference point for actual terror attack impact. 
    - Clearly labeling the axes will make it more user-friendly
* Comparing the change post attack to the stock's standard deviation will give you an idea if the movement is extreme for the stock (or index)
* Given that you have a small data set, it may be worth combining some of the terror attack types into groups. Such as linking transportation, utility, telecomm airlines, government into a public infrastructure. If you can find a logical link for grouping it may give you some insight into which areas of the economy are prone to causing ripple effects into the capital markets.
    - If you have time/interest it may be valuable to you to do some reading on how capital markets relate to an overall economy. Examining equity markets is very common, but bond markets are a much 'deeper' capital market. Given requirements to enter a capital market this sort of analysis is limited in its ability to capture effects on smaller firms.
* Creating a data frame of stock indices (by industry sector or market type) and listing the relevant terrorist attacks as dummy variables on their dates may give you a way to visualize the changes you're after. Running a linear regression on this set might be a good way to see how strong the relationship is between the attack incidents and stock movements.
    - This will work best if you can find which markets are responsive to what types of attacks (or attacks in general). The size of the US economy will likely make it less responsive to terrorist attacks when examined as a whole.
* This analysis has some interesting potential. Visualizing impacts of terror attacks should make for a cool presentation.