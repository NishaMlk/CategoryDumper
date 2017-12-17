# Category Dumper #

*Category Dumper* is a simple web crawler written in scrapy. It crawls through a website to find categories of items, and outputs them as JSON.

### *Demo Output* ###

	https://www.glassdoor.com/Jobs/University-of-California-Berkeley-Jobs-E32512.htm$Colleges & Universities|University of California Berkeley Jobs
	https://www.glassdoor.com/Jobs/University-of-Chicago-Jobs-E3016.htm$Colleges & Universities|University of Chicago Jobs
	https://www.glassdoor.com/Jobs/University-of-Florida-Jobs-E3017.htm$Colleges & Universities|University of Florida Jobs
	https://www.glassdoor.com/Jobs/University-of-Illinois-at-Urbana-Champaign-Jobs-E142738.htm$Colleges & Universities|University of Illinois at Urbana-Champaign Jobs
	https://www.glassdoor.com/Jobs/University-of-Maryland-Jobs-E129869.htm$Colleges & Universities|University of Maryland Jobs


### *Format of Output* ###

	{	
		"category" : <category name>,
		"company" : <company name>,
		"link" : <link to the section corresponding to this category>
	}


### *Demo of Configuration file* ###

	{
		"main_url":['https://www.glassdoor.com/sitedirectory/company-jobs.htm'],
		"allowed_domains":"glassdoor.com",
		"part_url":"https://www.glassdoor.com",

		"category_results": '//div[@id="PageLinks"][2]/div/ul/ul/li',
		"category_name":'span/a/text()',
		"category_path":'span/a/@href',

		"subcategory_results": '//ol/li[@class="header"]',
		"subcategory_name":'a/text()',
		"subcategory_path":'a/@href',
		"output_filename": "Glassdoor_cat.config"
	}
	
### *Configuration Parameters* ###

| Parameter         | Description |
|-------------------|-------------|
| main_url          | crawler starts at this url |
| allowed_domains   | set of urls which are allowed *used by scrapy* |
| part_url          | the category and sub-category paths may contain relative urls. They are contatinated with part_url to create an absolute url |
| subcategory_name  | xpath for the subcategory's name |
| subcategory_path  | xpath for the link to subcategory page |
| category_name     | xpath for the name of category  |
| category_path     | xpath for the link to category page |
| only_category     | boolean true if sub categories don't exist, false otherwise |
| output_filename   | outputs in the form of csv as needed by JobsCrawler in the form <link>$<category_name>|<subcategory_name> for each item |

### *Workflow of the CategoryDumper Spider* ###

1. Sets the starting url as `main_url`
2. Using the xpath from `category_name`, it creates a list of categories
3. For each category, it extracts the category name (from `category_name` xpath) and category link (from `category_path` xpath)
4. If sub categories don't exist (`only_category` is true), yields the category name and link
5. If sub categories do exist, it follows the sub category link ( from `subcategory_path`)
6. For each sub category, it yields the sub category name ( form `subcategory_name` xpath) and it's link (from `subcategory_path` xpath).

### How to run the project ? ###
1. Go to your folder and then type in following command  
>`D:\Repo>CategoryDumper> scrapy crawl categorydumper -afilename=glassdoor.config`