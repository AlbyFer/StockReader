from BorsaReader.Extractor_BorsaMilano import find_listing_milano



save_path = '/Users/albertoferrando/Google Drive/Progetti/Investimenti/BorsaReader/Storage/listino_milano.csv'
base = 'https://www.borse.it/quotazioni/borsa-italiana/listino-completo-azioni-italia'

listino = find_listing_milano(base, save_path)
