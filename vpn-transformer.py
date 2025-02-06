def transform_vpn(vpn: str, brand: str):
    """
    Transforms a single VPN into DAM search key and filename search key based on brand-specific rules.
    
    Args:
        vpn (str): A vendor part number.
        brand (str): The brand name.
    
    Returns:
        tuple: A tuple (brand, vpn, transformed_vpn)
    """
    if brand.lower() == "black diamond":
        if vpn.startswith("AP"):
            dam_search_key = f"{vpn[2:6]}_{vpn[6:9]}"
        elif vpn.startswith("BD"):
            dam_search_key = f"{vpn[2:8]}_{vpn[8:12]}"
        else:
            raise ValueError(f"Unsupported VPN format for Black Diamond: {vpn}")
        
        filename_search_key = dam_search_key  # Same as DAM search key for this brand
        return (brand, vpn, filename_search_key)
    
    else:
        raise ValueError("Brand transformation logic not implemented.")

def transform_vpns(vpns: list, brand: str):
    """
    Transforms a list of VPNs into DAM search keys and filename search keys based on brand-specific rules.
    
    Args:
        vpns (list): A list of vendor part numbers.
        brand (str): The brand name.
    
    Returns:
        list: A list of tuples (brand, vpn, transformed_vpn)
    """
    transformed_vpns = []
    
    for vpn in vpns:
        transformed_vpns.append(transform_vpn(vpn, brand))
    
    return transformed_vpns

# Example Usage
vpns = ["APZ9LC015LRG1", "BD58002493260601", "APCDT0426MED1", "AP7470220002LRG1", "AP7450414034LRG1", "BD6812291000ALL1", "BD6812290002ALL1", "BD6800881016ALL1", "AP7440639718LRG1"]
brand = "Black Diamond"

for transformed_vpn in transform_vpns(vpns, brand):
    print(transformed_vpn)  # Expected: [('Black Diamond', 'APZ9LC015LRG1', 'Z9LC_015'), ('Black Diamond', 'BD58002493260601', '580024_9326')]