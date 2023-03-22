# Proposal

## Motivation and Purpose

Role: Data scientist

Target audience: Concerned and/or prospective residents of Vancouver, BC

I am relatively new to Vancouver, BC, and I have not explored the city well enough. However, it seems that there are quite some preconcieved ideas on the crime rate of particular regions. I would like to see if particular regions really do contribute to "most crimes in town", and if it is, what type of crimes are those. To address this, this exploration will allow the users to facet the yearly data of the past 20 years, and facet them alongside offence types (e.g., mischief, homicide) and the neighbourhood.

## Description of the Data

The dataset used is a direct derivative of the [Crime Data](https://geodash.vpd.ca/opendata/), the open data published by the Vancouver Police Department (VPD) through their GeoDASH service. The raw dataset, between 2003 and 2022, there are 848,491 records, recording the date and time, hundred block, neighbourhood, coordinates (X and Y) as well as offence type. In this exploration we aggregate the raw data as 4,668 records, each record containing year, neighbourhood, type of offense, and the number of offences.

(Notice that the dataset does omit some crimes. The limitations are well-explained in the [Crime Data](https://geodash.vpd.ca/opendata/) page.)

## Research Questions and Usage Scenarios

Alex is considering moving to Vancouver, BC. He is not sure if the city is safe, as well as which districts are relatively safe. He first looks at the trend of number of crimes in the past 20 years to get a rough understanding. Then, he decides to break down the crime statistics to drill down and see which is the most common type of offence, and where it occurs the most. He also uses a heatmap to understand the relationship between offence type and the neighbourhood it occurs. With the help of this dashboard, he finds certain neighborhoods are becoming safer in the recent years. With the help of the dashboard, he shortlists the neighbourhoods he considers safe and starts looking for rentals in those regions.
