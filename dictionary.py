monthDict = {
    "Jan" :"January",
    "Feb" :"February",
    "Mar" :"March"
}

print(monthDict["Jan"])
print(monthDict.get("Nov", "Not Found"))

_check = {'detail' :'Invalid token.'}

if __name__ == "__main__" :
    if _check.get('detail') == "Invalid token." :
        print("YEP")
