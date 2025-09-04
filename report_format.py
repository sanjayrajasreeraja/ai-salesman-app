report_format = """
Generate a structured JSON array. Each element should follow this format:

{
  "Product Details": {
    "Product Name": "",
    "Nickname": "",
    "Category": "",
    "Scent": "",
    "Cost (INR)": "",
    "Stock": "",
    "Packaging Type": "",
    "Brand": "",
    "Usage": ""
  },
  "Business Entity Classification": {
    "Entity Type": "",
    "Location": "",
    "Retailer Name": ""
  },
  "Identified Business Issues": {
    "Payment Issues": "",
    "Purchase Issues": "",
    "Scheme Issues": "",
    "Display Issues": ""
  },
  "Market & Distributor Context": {
    "Market Intelligence": "",
    "Distributor Supply Issues": "",
    "Distributor Stock Issues": "",
    "Sales Return Issues": ""
  }
}

Return an array where each element corresponds to one mentioned product.
"""
