# Bayes Filter Demonstration with 2 Color Grid

How it works:
-The brightness of any grid-field indicates the probability of the true position (shown top right in blue color)
1) The probability of all the grid-fields shift along with the direction of the movement (with adjustable process noise)
2) After movement a measurement of color is taken, thus increase the probability of all those colors (with adjustable noise)
3) After gathering more and more information for every movement the localizer finally pinpoints the correct location
-The estimated position is then the position with the highest probability (shown top right in green color) 

>Bayes Filter with 2 Color Grid

![Bayes Filter](https://github.com/UmutCosk/Bayes-Filter-Localization/blob/master/showcase/example.gif)