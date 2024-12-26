from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)


liqueurs = ["Aloe Liqueur","Apricot Liqueur","Coconut Liqueur","Coffee Liqueur","Faretti Biscotti Famosi Liqueur","Kummel Liqueur","Maraschino Liqueur","Peach Liqueur","Pear Liqueur"]
fruits = ["Apple Slice","Banana Chip","Cherry","Cherry Tomato","Cucumber","Dehydrated Pineapple Slice","Dried Apple Slice","Grapefruit","Green Grape","Lemon","Lime","Orange","Peach Slice","Peach Puree","Pineapple","Raspberry","Seasonal Stone Fruit","Strawberry Halves"]
bitters=["Angostura Bitters","Bitter Truth Aromatic Bitters","Bitter Truth Jerry Thomas Bitters","Cardamom Bitters","Castilian Bitters","Celery Bitters","Grapefruit Bitters","Lavender Bitters","Orange Bitters","Mole Bitters","Peychaud's Bitters","Toasted Pecan Bitters"]
syrups=["Basil Stem Syrup","Cane Sugar Syrup","Cinnamon Syrup","Clarified Strawberry Syrup","Demerara Gum Syrup","Ginger Syrup","Grilled Pineapple Syrup","Honey Syrup","Maple Syrup","Pineapple Gum Syrup","Raisin Honey Syrup","Simple Syrup","Strawberry Cream Syrup","White Honey Syrup"]
non_alc_liquids=["Almond Milk","Apple Celery Soda","Apple Cider","Apple Juice","Coca Cola","Coconut Cream","Coconut Milk (unsweetened)","Coffee","Cranberry Juice","Eucalyptus Extract","Grapefruit Soda","Half and Half","Heavy Cream","Hot Milk","Ice Cream","Orange Extract","Orange Flower Water","Orange Marmalade","Root Beer Extract","Seltzer","Tonic Water","Vanilla","Clarified Cucumber Water","Clarified Lime Juice"]
solutions = ["Champagne Acid Solution","Citric Acid Solution","Lactic Acid Solution","Phosphoric Acid Solution","Rosemary Salt Solution","Salt Solution","Sel Gris Solution"]
garnishes = ["Basil Leaf","Brandied Cherry","Candied Ginger","Candy Cane","Celery Ribbon","Cereal","Cherry Wood Chips","Cinnamon","Cinnamon Stick","Coffee Beans","Confectioners' Sugar","Dark Chocolate","Demerara Sugar","Edible Flower","Mint Sprig","Olive","Nutmeg","Sugar Cube","Toasted Coconut Chips","Thyme sprig","Sage"]
mixes = ["Bloody Mary Mix","Don's Mix No. 1","Tom and Jerry Batter","Verde Mix"]
amari = ["Amaretto","Amaro Abano","Amaro CioCiaro","Amaro di Angostura","Amaro Meletti","Amaro Montenegro","Amaro Nardini","Amaro Nonino"]
crema = ["Creme Yvette","Creme de Cacao","Creme de Cassis","Creme de menthe","Creme de Peche","Creme de Pamplemousse","Creme de Violette"]
eggs=["Egg White","Egg (whole)","Egg White"]
alcs=["Abrigot du Roussillon","Absinthe","Amer","Aperol","Aquavit","Bailey's Irish Cream","Banane du Bresil","Bas-Armagnac","Beer","Benedictine","Bourbon","Brandy","Cachaca","Calvados","Campari","Cassis Noir du Bourgogne","Cava","Champagne","Chardonnay","Chartreuse","Cherry Heering","Cocchi Americano","Cointreau","Cognac","Curacao","Cynar","Dolin Blanc","Dram","Eau de Vie","Galliano l'Autentico","Galliano Ristretto","Gin","Grand Mariner","Grapefruit Cordial","Grappa","Grenadine","Lemon Cordial","Limoncello","Lillet blanc","Lillet Rose","Orgeat","Madeira","Menthe-Pastille","Mezcal","Pilsner","Pineau des Charentes","Pisco","Port","Ramazzotti","Rose Cremant","Royal Combier","Rum","Rye","Sake","Salers Gentiane","Scotch","Sherry","Singani 63","Spirit","St-Germain","Strega","Suze","Tailor Velvet Falernum","Tequila","Tincture","Vermouth","Verjus","Vodka","Whiskey","White Wine"]

all_ingredients = liqueurs+fruits+bitters+syrups+non_alc_liquids+solutions+garnishes+mixes+amari+crema+eggs+alcs

with open("t1.csv","r") as file:
    df = pd.read_csv(file,delimiter=",")

@app.route("/")
def setup():
    result = []
    return render_template("frontend.html",results=result,alcs=alcs, r_disp="",given_ingr="")

def OR(df, requests):
    filtered_df = pd.DataFrame([])
    for item in requests:
        curr_df = df[df[item]>0]
        filtered_df = pd.concat([filtered_df, curr_df])
    return filtered_df

def AND(df, requests):
    results = pd.DataFrame([])
    filtered_df = df.copy(deep=True)
    for i, row in df.iterrows():
        good=True
        for alc in all_ingredients:
            if row[alc]>0 and alc not in requests:
                good=False
                # print("dropping")
                # print("filtered_df before: ",filtered_df)
                # filtered_df.drop([i],inplace=True)
                # filtered_df = filtered_df.reindex_like(df[:-i])
                # print("filtered df: ",filtered_df)
        if good:
            print("yes")
            results = pd.concat([results, pd.DataFrame([row])])
            print(results)
    return results

def OUT(filtered_df,all_ingredients):
    results = []
    i=-1
    for index, row in filtered_df.iterrows():
        i+=1
        results.append([0,[],0])
        print(results)
        results[i][0] = row["Name"]
        results[i][2] = row["Info"]
        
        for alc in all_ingredients:
            if alc not in row:
                print(alc,"not in the row???")
                pass
            elif row[alc] > 0:
                AMT = f'{alc} AMT'
                EQ = f'{alc} EQ'
                if (EQ in df.columns) and (AMT in df.columns):
                    results[i][1].append(f'{alc}: \n\t{row[alc]} {row[AMT]}, {row[EQ]}')
                elif (EQ in df.columns):
                    results[i][1].append(f'{alc}: \n\t{row[alc]} {row[EQ]}')
                elif (AMT in df.columns) and (EQ not in df.columns):
                    results[i][1].append(f'{alc}: \n\t{row[alc]} {row[AMT]}')
                else:
                    results[i][1].append(f'{alc}: \n\t{row[alc]}')
    return results

@app.route("/test", methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        requests = [val for key, val in request.form.items()]
        if requests[0]=="See all drinks containing these ingredients":
            print("OR")
            filtered_df = OR(df, requests[2:])
        else:
            print("AND")
            filtered_df = AND(df, requests[2:])
        results = OUT(filtered_df, all_ingredients)
        # print("\n\n\nresults:",results,"\n\n\n")

        return render_template("frontend.html",results=results, r_disp="Results",given_ingr=f"Given Ingredients: {requests}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
