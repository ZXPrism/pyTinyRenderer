class Model:

    triangleNum = 0
    modelData = []

    def __init__(self, wavefrontOBJFilePath: str):
        obj = open(wavefrontOBJFilePath)
        lines = obj.readlines()
        obj.close()

        coords = [[]]
        texCoords = [[]]
        normalCoords = [[]]

        for line in lines:
            item = line.strip().split()

            if len(item) == 0:
                continue

            if item[0][0] == "v":  # v
                if len(item[0]) == 1:
                    pos = list(map(float, item[1:]))
                    coords.append(pos)
                elif item[0][1] == "t":  # vt
                    pos = list(map(float, item[1:]))
                    texCoords.append(pos)
                else:  # vn
                    pos = list(map(float, item[1:]))
                    normalCoords.append(pos)

            elif item[0] == "f":
                faceVerticesIdx = [i.split("/") for i in item[1:]]
                faceData = []

                # Parse face data
                # ORDER: vertex coord - tex coord - normal coord
                # e.g. modelData = [..., [x, y, z], [x, y], [x, y, z], ...]
                for i in range(3):
                    faceData.append(coords[int(faceVerticesIdx[i][0])])
                    faceData.append(texCoords[int(faceVerticesIdx[i][1])])
                    faceData.append(normalCoords[int(faceVerticesIdx[i][2])])

                self.modelData.extend(faceData)
                self.triangleNum += 1
