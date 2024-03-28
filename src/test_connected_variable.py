from connected_variables import ConnectedVariables

cv = ConnectedVariables()
cv.define('a', 1)
while 1:
    cv.heart_beat()