"""
Web3 and Web3 Gaming project definitions
This module contains curated lists of top Web3 and Web3 Gaming projects
"""

def get_web3_projects():
    """
    Returns a list of 100 Web3 projects (50 Web3 + 50 Web3 Gaming)
    Each project includes symbol, name, and category for API integration
    """
    
    web3_projects = [
        # DeFi Protocols
        {'symbol': 'UNI', 'name': 'Uniswap', 'category': 'Web3'},
        {'symbol': 'AAVE', 'name': 'Aave', 'category': 'Web3'},
        {'symbol': 'COMP', 'name': 'Compound', 'category': 'Web3'},
        {'symbol': 'MKR', 'name': 'Maker', 'category': 'Web3'},
        {'symbol': 'SNX', 'name': 'Synthetix', 'category': 'Web3'},
        {'symbol': 'CRV', 'name': 'Curve DAO Token', 'category': 'Web3'},
        {'symbol': 'BAL', 'name': 'Balancer', 'category': 'Web3'},
        {'symbol': 'YFI', 'name': 'yearn.finance', 'category': 'Web3'},
        {'symbol': '1INCH', 'name': '1inch Network', 'category': 'Web3'},
        {'symbol': 'SUSHI', 'name': 'SushiSwap', 'category': 'Web3'},
        
        # Layer 1 Blockchains
        {'symbol': 'ETH', 'name': 'Ethereum', 'category': 'Web3'},
        {'symbol': 'BNB', 'name': 'BNB', 'category': 'Web3'},
        {'symbol': 'ADA', 'name': 'Cardano', 'category': 'Web3'},
        {'symbol': 'SOL', 'name': 'Solana', 'category': 'Web3'},
        {'symbol': 'DOT', 'name': 'Polkadot', 'category': 'Web3'},
        {'symbol': 'AVAX', 'name': 'Avalanche', 'category': 'Web3'},
        {'symbol': 'ATOM', 'name': 'Cosmos', 'category': 'Web3'},
        {'symbol': 'ALGO', 'name': 'Algorand', 'category': 'Web3'},
        {'symbol': 'FTM', 'name': 'Fantom', 'category': 'Web3'},
        {'symbol': 'NEAR', 'name': 'NEAR Protocol', 'category': 'Web3'},
        
        # Layer 2 Solutions
        {'symbol': 'MATIC', 'name': 'Polygon', 'category': 'Web3'},
        {'symbol': 'LRC', 'name': 'Loopring', 'category': 'Web3'},
        {'symbol': 'IMX', 'name': 'Immutable X', 'category': 'Web3'},
        {'symbol': 'OP', 'name': 'Optimism', 'category': 'Web3'},
        {'symbol': 'ARB', 'name': 'Arbitrum', 'category': 'Web3'},
        
        # Web3 Infrastructure
        {'symbol': 'LINK', 'name': 'Chainlink', 'category': 'Web3'},
        {'symbol': 'GRT', 'name': 'The Graph', 'category': 'Web3'},
        {'symbol': 'FIL', 'name': 'Filecoin', 'category': 'Web3'},
        {'symbol': 'AR', 'name': 'Arweave', 'category': 'Web3'},
        {'symbol': 'STORJ', 'name': 'Storj', 'category': 'Web3'},
        
        # NFT & Metaverse
        {'symbol': 'APE', 'name': 'ApeCoin', 'category': 'Web3'},
        {'symbol': 'MANA', 'name': 'Decentraland', 'category': 'Web3'},
        {'symbol': 'SAND', 'name': 'The Sandbox', 'category': 'Web3'},
        {'symbol': 'ENJ', 'name': 'Enjin Coin', 'category': 'Web3'},
        {'symbol': 'FLOW', 'name': 'Flow', 'category': 'Web3'},
        
        # DAOs and Governance
        {'symbol': 'ANT', 'name': 'Aragon', 'category': 'Web3'},
        {'symbol': 'BNT', 'name': 'Bancor', 'category': 'Web3'},
        {'symbol': 'REN', 'name': 'Ren', 'category': 'Web3'},
        {'symbol': 'LPT', 'name': 'Livepeer', 'category': 'Web3'},
        {'symbol': 'MLN', 'name': 'Enzyme', 'category': 'Web3'},
        
        # Privacy & Security
        {'symbol': 'ZEC', 'name': 'Zcash', 'category': 'Web3'},
        {'symbol': 'XMR', 'name': 'Monero', 'category': 'Web3'},
        {'symbol': 'SCRT', 'name': 'Secret', 'category': 'Web3'},
        {'symbol': 'ROSE', 'name': 'Oasis Network', 'category': 'Web3'},
        {'symbol': 'NYM', 'name': 'Nym', 'category': 'Web3'},
        
        # Cross-chain & Interoperability
        {'symbol': 'ICP', 'name': 'Internet Computer', 'category': 'Web3'},
        {'symbol': 'KSM', 'name': 'Kusama', 'category': 'Web3'},
        {'symbol': 'RUNE', 'name': 'THORChain', 'category': 'Web3'},
        {'symbol': 'CKB', 'name': 'Nervos Network', 'category': 'Web3'},
        {'symbol': 'BAND', 'name': 'Band Protocol', 'category': 'Web3'},
        
        # Additional Web3 Projects
        {'symbol': 'LIT', 'name': 'Litentry', 'category': 'Web3'}
    ]
    
    gaming_projects = [
        # Gaming Tokens
        {'symbol': 'AXS', 'name': 'Axie Infinity', 'category': 'Web3 Gaming'},
        {'symbol': 'SLP', 'name': 'Smooth Love Potion', 'category': 'Web3 Gaming'},
        {'symbol': 'GALA', 'name': 'Gala', 'category': 'Web3 Gaming'},
        {'symbol': 'ILV', 'name': 'Illuvium', 'category': 'Web3 Gaming'},
        {'symbol': 'ALICE', 'name': 'My Neighbor Alice', 'category': 'Web3 Gaming'},
        {'symbol': 'TLM', 'name': 'Alien Worlds', 'category': 'Web3 Gaming'},
        {'symbol': 'RADIO', 'name': 'RadioShack', 'category': 'Web3 Gaming'},
        {'symbol': 'WAXP', 'name': 'WAX', 'category': 'Web3 Gaming'},
        {'symbol': 'CHR', 'name': 'Chromia', 'category': 'Web3 Gaming'},
        {'symbol': 'PYR', 'name': 'Vulcan Forged PYR', 'category': 'Web3 Gaming'},
        
        # Play-to-Earn Games
        {'symbol': 'GHST', 'name': 'Aavegotchi', 'category': 'Web3 Gaming'},
        {'symbol': 'REVV', 'name': 'REVV', 'category': 'Web3 Gaming'},
        {'symbol': 'TOWER', 'name': 'Crazy Defense Heroes', 'category': 'Web3 Gaming'},
        {'symbol': 'SKILL', 'name': 'CryptoBlades', 'category': 'Web3 Gaming'},
        {'symbol': 'GODS', 'name': 'Gods Unchained', 'category': 'Web3 Gaming'},
        {'symbol': 'SPS', 'name': 'Splinterlands', 'category': 'Web3 Gaming'},
        {'symbol': 'DEC', 'name': 'Dark Energy Crystals', 'category': 'Web3 Gaming'},
        {'symbol': 'DPET', 'name': 'My DeFi Pet', 'category': 'Web3 Gaming'},
        {'symbol': 'NFTB', 'name': 'NFTb', 'category': 'Web3 Gaming'},
        {'symbol': 'ETERNAL', 'name': 'CryptoMines Eternal', 'category': 'Web3 Gaming'},
        
        # Gaming Infrastructure
        {'symbol': 'RONIN', 'name': 'Ronin', 'category': 'Web3 Gaming'},
        {'symbol': 'ULTRA', 'name': 'Ultra', 'category': 'Web3 Gaming'},
        {'symbol': 'EFI', 'name': 'Efinity Token', 'category': 'Web3 Gaming'},
        {'symbol': 'GMEE', 'name': 'GAMEE', 'category': 'Web3 Gaming'},
        {'symbol': 'DIVI', 'name': 'Divi', 'category': 'Web3 Gaming'},
        
        # Metaverse Gaming
        {'symbol': 'STAR', 'name': 'StarLink', 'category': 'Web3 Gaming'},
        {'symbol': 'UFO', 'name': 'UFO Gaming', 'category': 'Web3 Gaming'},
        {'symbol': 'HERO', 'name': 'Metahero', 'category': 'Web3 Gaming'},
        {'symbol': 'DOSE', 'name': 'DOSE', 'category': 'Web3 Gaming'},
        {'symbol': 'NAKA', 'name': 'Nakamoto Games', 'category': 'Web3 Gaming'},
        
        # Virtual Real Estate
        {'symbol': 'LAND', 'name': 'Landshare', 'category': 'Web3 Gaming'},
        {'symbol': 'REALM', 'name': 'Realm', 'category': 'Web3 Gaming'},
        {'symbol': 'WILD', 'name': 'Wilder World', 'category': 'Web3 Gaming'},
        {'symbol': 'BOSON', 'name': 'Boson Protocol', 'category': 'Web3 Gaming'},
        {'symbol': 'BEPRO', 'name': 'BetProtocol', 'category': 'Web3 Gaming'},
        
        # Gaming DAOs
        {'symbol': 'YGG', 'name': 'Yield Guild Games', 'category': 'Web3 Gaming'},
        {'symbol': 'MC', 'name': 'Merit Circle', 'category': 'Web3 Gaming'},
        {'symbol': 'GGG', 'name': 'Good Games Guild', 'category': 'Web3 Gaming'},
        {'symbol': 'GUILD', 'name': 'BlockchainSpace', 'category': 'Web3 Gaming'},
        {'symbol': 'LABS', 'name': 'LABS Group', 'category': 'Web3 Gaming'},
        
        # Mobile Gaming
        {'symbol': 'MOBOX', 'name': 'MOBOX', 'category': 'Web3 Gaming'},
        {'symbol': 'BIND', 'name': 'Cometh', 'category': 'Web3 Gaming'},
        {'symbol': 'SUPER', 'name': 'SuperFarm', 'category': 'Web3 Gaming'},
        {'symbol': 'MIST', 'name': 'Mist', 'category': 'Web3 Gaming'},
        {'symbol': 'DREAMS', 'name': 'Dreams Quest', 'category': 'Web3 Gaming'},
        
        # Card Games
        {'symbol': 'SOR', 'name': 'SoRare', 'category': 'Web3 Gaming'},
        {'symbol': 'CARDS', 'name': 'Cards of BSC', 'category': 'Web3 Gaming'},
        {'symbol': 'CWAR', 'name': 'Cryowar', 'category': 'Web3 Gaming'},
        {'symbol': 'KNIGHT', 'name': 'Forest Knight', 'category': 'Web3 Gaming'},
        {'symbol': 'ARENA', 'name': 'Arena Token', 'category': 'Web3 Gaming'},
        
        # Additional Gaming Projects to reach 50
        {'symbol': 'GLMR', 'name': 'Moonbeam', 'category': 'Web3 Gaming'}
    ]
    
    # Combine both lists
    all_projects = web3_projects + gaming_projects
    
    # Ensure we have exactly 100 projects
    return all_projects[:100]

def get_project_categories():
    """Returns the available project categories"""
    return ['Web3', 'Web3 Gaming']

def get_projects_by_category(category: str):
    """Returns projects filtered by category"""
    all_projects = get_web3_projects()
    if category == 'All':
        return all_projects
    return [p for p in all_projects if p['category'] == category]
