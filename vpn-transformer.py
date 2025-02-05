def transform_vpn(vpn: str, brand: str):
    """
    Transforms a given VPN into DAM search key and filename search key based on brand-specific rules.
    
    Args:
        vpn (str): The vendor part number.
        brand (str): The brand name.
    
    Returns:
        tuple: (dam_search_key, filename_search_key)
    """
    if brand.lower() == "black diamond":
        if vpn.startswith("AP"):
            dam_search_key = f"{vpn[2:6]}_{vpn[6:9]}"
        elif vpn.startswith("BD"):
            dam_search_key = f"{vpn[2:8]}_{vpn[8:12]}"
        else:
            raise ValueError("Unsupported VPN format for Black Diamond.")
        
        filename_search_key = dam_search_key  # Same as DAM search key for this brand
        return dam_search_key, filename_search_key
    
    else:
        raise ValueError("Brand transformation logic not implemented.")

# Example Usage
vpn1 = "APZ9LC015LRG1"
vpn2 = "BD58002493260601"
brand = "Black Diamond"

print(transform_vpn(vpn1, brand))  # Expected: ('Z9LC_015', 'Z9LC_015')
print(transform_vpn(vpn2, brand))  # Expected: ('580024_9326', '580024_9326')
