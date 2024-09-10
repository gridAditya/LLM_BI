advanced_monthly_sales_for_retail_and_food_services_schema = '''
[
	{
		"Field" : "id",
		"Type" : "bigint",
		"Null" : "NO",
		"Key" : "PRI",
		"Default" : None,
		"Extra" : "auto_increment"
	},
	{
		"Field" : "category_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["452","4521E","453","44Y72","44Z72","451","454","722","44000","441","444","445","4451","446","447","448","441X","442","443","44X72","44W72"]
	},
	{
		"Field" : "cell_value",
		"Type" : "double",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value": "long string in this"
	},
	{
		"Field" : "data_type_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["SM","MPCSM","E_SM","E_MPCSM"]

	},
	{
		"Field" : "error_data",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["no","yes"]
	},
	{
		"Field" : "seasonally_adj",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["yes","no"]
	},
	{
		"Field" : "time",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "here is time in format yyyy-mm"
	},
	{
		"Field" : "time_slot_id",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":[0]
	},
	{
		"Field" : "us",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["US"]
	}
]
'''

advanced_monthly_sales_for_retail_and_food_services_categories_schema = '''
[
	{
		"Field" : "cat_idx",
		"Type" : "int",
		"Null" : "NO",
		"Key" : "PRI",
		"Default" : None,
		"Extra" : ""
	},
	{
		"Field" : "cat_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value": ["44X72","44Y72","44Z72","44W72","44000","441","441X","442","443","444","445","4451","446","447","448","451","452","4521E","453","454","722"]
	},
	{
		"Field" : "cat_desc",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["44X72: Retail Trade and Food Services","44Y72: Retail Trade and Food Services, ex Auto","44Z72: Retail Trade and Food Services, ex Gas","44W72: Retail Trade and Food Services, ex Auto and Gas","44000: Retail Trade","441: Motor Vehicle and Parts Dealers","4411,4412: Auto and Other Motor Vehicles","442: Furniture and Home Furnishings Stores","443: Electronics and Appliance Stores","444: Building Mat. and Garden Equip. and Supplies Dealers","445: Food and Beverage Stores","4451: Grocery Stores","446: Health and Personal Care Stores","447: Gasoline Stations","448: Clothing and Clothing Access. Stores","451: Sporting Goods, Hobby, Musical Instrument, and Book Stores","452: General Merchandise Stores","4521: Department Stores","453: Miscellaneous Store Retailers","454: Nonstore Retailers","722: Food Services and Drinking Places"]
    }
]
'''

advanced_monthly_sales_for_retail_and_food_services_data_types_schema = '''
[
	{
		"Field" : "dt_idx",
		"Type" : "int",
		"Null" : "NO",
		"Key" : "PRI",
		"Default" : None,
		"Extra" : ""
	},
	{
		"Field" : "dt_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["SM","MPCSM"]
	},
	{
		"Field" : "dt_desc",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["Sales - Monthly","Sales - Monthly Percent Change"]
	}
]
'''

housing_vacancies_and_homeownership_schema = '''
[
	{
		"Field" : "id",
		"Type" : "bigint",
		"Null" : "NO",
		"Key" : "PRI",
		"Default" : None,
		"Extra" : "auto_increment"
	},
	{
		"Field" : "category_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["RATE","ESTIMATE"]
	},
	{
		"Field" : "cell_value",
		"Type" : "double",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : ""
	},
	{
		"Field" : "data_type_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["HOR","E_HOR","HVR","E_HVR","RVR","E_RVR","SAHOR","OCCUSE","OFFMAR","OTH","SEASON","URE","OWNOCC","RENT","RNTOCC","RNTSLD","SALE","TOTAL","VACANT","YRVAC","OCC"]

	},
	{
		"Field" : "error_data",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["no","yes"]
	},
	{
		"Field" : "seasonally_adj",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["no","yes"]
	},
	{
		"Field" : "time",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "here is the time in format yyyy-Q1, yyyy-Q2, yyyy-Q3, yyyy-Q4 here is the Q is for Quarter"
	},
	{
		"Field" : "time_slot_id",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":"0"
	}
]
'''

housing_vacancies_and_homeownership_categories_schema = '''
[
	{
		"Field" : "cat_idx",
		"Type" : "int",
		"Null" : "NO",
		"Key" : "PRI",
		"Default" : None,
		"Extra" : ""
       
	},
	{
		"Field" : "cat_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["RATE","ESTIMATE"]
        
	},
	{
		"Field" : "cat_desc",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["Rate","Housing Inventory Estimate"]
	}
]
'''

housing_vacancies_and_homeownership_data_types_schema = '''
[
	{
		"Field" : "dt_idx",
		"Type" : "int",
		"Null" : "NO",
		"Key" : "PRI",
		"Default" : None,
		"Extra" : ""
	},
	{
		"Field" : "dt_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["RVR","HVR","HOR","SAHOR","TOTAL","OCC","OWNOCC","RNTOCC","VACANT","YRVAC","SEASON","RENT","SALE","RNTSLD","OFFMAR","OCCUSE","URE","OTH"]        
	},
	{
		"Field" : "dt_desc",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["Rental Vacancy Rate","Homeowner Vacancy Rate","Homeownership Rate","Seasonally Adjusted Homeownership Rate","Total Housing Units","Occupied Housing Units","Owner Occupied Housing Units","Renter Occupied Housing Units","Vacant Housing Units","Year-Round Vacant Housing Units","Seasonal Housing Units","Vacant Housing Units for Rent","Vacant Housing Units for Sale","Vacant Housing Units Rented or Sold,Not Yet Occupied","Vacant Housing Units Held Off the Market","Vacant Housing Units Held Off the Market and For Occasional Use","Vacant Housing Units Held Off the Market and Usual Residence Elsewhere","Vacant Housing Units Held Off the Market and Vacant for Other Reasons"]
    }
]
'''

international_trade_schema = '''
[
	{
		"Field" : "id",
		"Type" : "bigint",
		"Null" : "NO",
		"Key" : "PRI",
		"Default" : None,
		"Extra" : "auto_increment"
	},
	{
		"Field" : "category_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["BOPG","BOPGS"]
	},
	{
		"Field" : "cell_value",
		"Type" : "double",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : ""
	},
	{
		"Field" : "data_type_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["BAL","EXP","IMP"]
	},
	{
		"Field" : "error_data",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["no"]
	},
	{
		"Field" : "seasonally_adj",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["no","yes"]
	},
	{
		"Field" : "time",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "here is time in format yyyy-mm"
	},
	{
		"Field" : "time_slot_id",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["0"]
	},
	{
		"Field" : "us",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["US"]
	}
]
'''

international_trade_categories_schema = '''
[
	{
		"Field" : "cat_idx",
		"Type" : "int",
		"Null" : "NO",
		"Key" : "PRI",
		"Default" : None,
		"Extra" : ""
	},
	{
		"Field" : "cat_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["BOPGS","BOPG"]
	},
	{
		"Field" : "cat_desc",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["Balance of Payment Goods and Services","Balance of Payment Goods"]
	}
]
'''

international_trade_data_types_schema = '''
[
	{
		"Field" : "dt_idx",
		"Type" : "int",
		"Null" : "NO",
		"Key" : "PRI",
		"Default" : None,
		"Extra" : ""
	},
	{
		"Field" : "dt_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["BAL","EXP","IMP"]
	},
	{
		"Field" : "dt_desc",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["Balance","Exports","Imports"]
	}
]
'''

manufacturers_shipments_inventories_and_orders_schema = '''
[
	{
		"Field" : "id",
		"Type" : "bigint",
		"Null" : "NO",
		"Key" : "PRI",
		"Default" : None,
		"Extra" : "auto_increment"
	},
	{
		"Field" : "category_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["35S","CDG","MNM","11S","12S","23S","31S","34J","22S","31C","33I","12A","34I","33M","25S","33D","34D","16S","21S","26S","33E","33G","34E","11A","11B","27S","34F","15S","33C","14S","24S","25A","33S","13S","34B","24A","32S","25C","34A","25B","33A","34S","36Z","DAP","MTU","22B","31A","33H","36S","CRP","MTM","34K","COG","TGP","11C","22A","34H","35C","39S","ITI","NAP","DXT","BTP","MDM","NXA","DEF","MVP","35A","37S","DXD","34X","MXD","35D","ANM","NDE","35B","36B","CMS","CNG","TCG","36A","12B","34C","36C","MXT","ODG"]
	},
	{
		"Field" : "cell_value",
		"Type" : "double",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : ""
	},
	{
		"Field" : "data_type_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["US","NO","FI","TI","MPCFI","MPCMI","MPCNO","MPCTI","MPCVS","VS","UO","MPCUO","WI","IS","MPCWI","MI"]
	},
	{
		"Field" : "error_data",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["no"]
	},
	{
		"Field" : "seasonally_adj",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["no","yes"]
	},
	{
		"Field" : "time",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "here is time in format yyyy-mm"
	},
	{
		"Field" : "time_slot_id",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["0"]
	},
	{
		"Field" : "us",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["US"]
	}
]
'''

manufacturers_shipments_inventories_and_orders_categories_schema = '''
[
	{
		"Field" : "cat_idx",
		"Type" : "int",
		"Null" : "NO",
		"Key" : "PRI",
		"Default" : None,
		"Extra" : ""
	},
	{
		"Field" : "cat_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["MTM","MXT","MXD","MTU","MDM","21S","27S","31S","31A","ANM","31C","32S","33S","33A","33C","33D","33E","33G","33H","33I","TGP","33M","34S","34A","34B","34C","34D","34E","34F","34G","34H","34I","34J","34K","35S","35A","35B","35C","35D","36S","36A","36B","36C","BTP","NAP","DAP","36Z","37S","39S","MNM","11S","11A","11B","11C","12S","12A","12B","13S","14S","15S","16S","22S","22A","22B","23S","24S","24A","25S","25A","25B","25C","26S","CMS","ITI","CRP","MVP","TCG","NDE","NXA","DEF","COG","CDG","CNG","DXT","DXD","34X","ODG"]
	},
	{
		"Field" : "cat_desc",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["Total Manufacturing","Manufacturing Excluding Transportation","Manufacturing Excluding Defense","Manufacturing with Unfilled Orders","Durable Goods","Wood Products","Nonmetallic Mineral Products","Primary Metals","Iron and Steel Mills and Ferroalloy and Steel Product Manufacturing","Aluminum and Nonferrous Metal Products","Ferrous Metal Foundries","Fabricated Metal Products","Machinery","Farm Machinery and Equipment Manufacturing","Construction Machinery Manufacturing","Mining, Oil, and Gas Field Machinery Manufacturing","Industrial Machinery Manufacturing","Photographic Equipment Manufacturing","Ventilation, Heating, Air-conditioning, and Refrigeration Equipment Manufacturing","Metalworking Machinery Manufacturing","Turbines, Generators, and Other Power Transmission Equipment","Material Handling Equipment Manufacturing","Computer and Electronic Products","Electronic Computer Manufacturing","Computer Storage Device Manufacturing","Other Computer Peripheral Equipment Manufacturing","Communications Equipment Manufacturing, Nondefense","Communications Equipment Manufacturing, Defense","Audio and Video Equipment","Semiconductor and Related Device Manufacturing","Other Electronic Component Manufacturing","Search and Navigation Equipment, Nondefense","Search and Navigation Equipment, Defense","Electromedical, Measuring, and Control Instrument Manufacturing","Electrical Equipment, Appliances and Components","Electric Lighting Equipment Manufacturing","Household Appliance Manufacturing","Electrical Equipment Manufacturing","Battery Manufacturing","Transportation Equipment","Automobile Manufacturing","Light Truck and Utility Vehicle Manufacturing","Heavy Duty Truck Manufacturing","Motor Vehicle Bodies, Trailers, and Parts","Nondefense Aircraft and Parts","Defense Aircraft and Parts","Ships and Boats","Furniture and Related Products","Miscellaneous Products","Nondurable Goods","Food Products","Grain and Oilseed Milling","Dairy Product Manufacturing","Meat, Poultry, and Seafood Product Processing","Beverage and Tobacco Products","Beverage Manufacturing","Tobacco Manufacturing","Textile Mills","Textile Products","Apparel","Leather and Allied Products","Paper Products","Pulp, Paper, and Paperboard Mills","Paperboard Container Manufacturing","Printing","Petroleum and Coal Products","Petroleum Refineries","Chemical Products","Pesticide, Fertilizer, and Other Agricultural Chemical Manufacturing","Pharmaceutical and Medicine Manufacturing","Paint, Coating, and Adhesive, Manufacturing","Plastics and Rubber Products","Construction Materials and Supplies","Information Technology Industries","Computers and Related Products","Motor Vehicles and Parts","Capital Goods","Nondefense Capital Goods","Nondefense Capital Goods Excluding Aircraft","Defense Capital Goods","Consumer Goods","Consumer Durable Goods","Consumer Nondurable Goods","Durable Goods Excluding Transportation","Durable Goods Excluding Defense","Communication Equipment","Other Durable Goods"]
	}
]
'''

manufacturers_shipments_inventories_and_orders_data_types_schema = '''
[
	{
		"Field" : "dt_idx",
		"Type" : "int",
		"Null" : "NO",
		"Key" : "PRI",
		"Default" : None,
		"Extra" : ""
	},
	{
		"Field" : "dt_code",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["VS","NO","UO","TI","MI","WI","FI","IS","US","MPCVS","MPCNO","MPCUO","MPCTI","MPCMI","MPCWI","MPCFI"]
	},
	{
		"Field" : "dt_desc",
		"Type" : "varchar(255)",
		"Null" : "YES",
		"Key" : "",
		"Default" : None,
		"Extra" : "",
        "unique_value":["Value of Shipments","New Orders","Unfilled Orders","Total Inventories","Materials and Supplies Inventories","Work in Process Inventories","Finished Goods Inventories","Inventories to Shipments Ratios","Unfilled Orders to Shipments Ratios","Value of Shipments Percent Change Monthly","New Orders Percent Change Monthly","Unfilled Orders Percent Change Monthly","Total Inventories Percent Change Monthly","Materials & Supplies Inventories Percent Change Monthly","Work in Progress Inventories Percent Change Monthly","Finished Goods Inventories Percent Change Monthly"]
	}
]
'''

schema = {

    "advanced_monthly_sales_for_retail_and_food_services": advanced_monthly_sales_for_retail_and_food_services_schema,
    "advanced_monthly_sales_for_retail_and_food_services_categories": advanced_monthly_sales_for_retail_and_food_services_categories_schema,
    "advanced_monthly_sales_for_retail_and_food_services_data_types": advanced_monthly_sales_for_retail_and_food_services_data_types_schema,

    "housing_vacancies_and_homeownership": housing_vacancies_and_homeownership_schema,
    "housing_vacancies_and_homeownership_categories": housing_vacancies_and_homeownership_categories_schema,
    "housing_vacancies_and_homeownership_data_types": housing_vacancies_and_homeownership_data_types_schema,

    "international_trade": international_trade_schema,
    "international_trade_categories": international_trade_categories_schema,
    "international_trade_data_types": international_trade_data_types_schema,

    "manufacturers_shipments_inventories_and_orders": manufacturers_shipments_inventories_and_orders_schema,
    "manufacturers_shipments_inventories_and_orders_categories": manufacturers_shipments_inventories_and_orders_categories_schema,
    "manufacturers_shipments_inventories_and_orders_data_types": manufacturers_shipments_inventories_and_orders_data_types_schema,
}
