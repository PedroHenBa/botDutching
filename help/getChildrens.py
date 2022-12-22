
def getChildrens(driver, element):
    children = driver.execute_script("""
                var parent = arguments[0];
                var child = parent.firstChild;
                var ret = "";
                while(child) {
                    if (child.nodeType === Node.TEXT_NODE)
                        ret += child.textContent;
                    child = child.nextSibling;
                }
                return ret;
                """, element)
    return children