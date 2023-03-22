bl_info = {
    "name": "ChatGPT Blender",
    "author": "Davi Teodoro, ChatGPT",
    "version": (1, 3),
    "blender": (2, 80, 0),
    "location": "View3D > N-Panel",
    "description": "Comunique-se com ChatGPT para executar comandos no Blender",
    "category": "3D View",
}

import urllib.request
import urllib.error
import bpy
import json

def create_geometry_nodes_from_dict(node_tree_name, node_tree_data):
    node_tree = bpy.data.node_groups.new(node_tree_name, "GeometryNodeTree")

    nodes = {}
    for node_data in node_tree_data["nodes"]:
        node = node_tree.nodes.new(node_data["type"])
        node.name = node_data["name"]
        node.location.x, node.location.y = node_data["location"]

        for prop_name, prop_value in node_data["properties"].items():
            if hasattr(node, prop_name):
                try:
                    setattr(node, prop_name, prop_value)
                except AttributeError:
                    pass

        nodes[node.name] = node

    for link_data in node_tree_data["links"]:
        from_node = nodes[link_data["from_node"]]
        from_socket = from_node.outputs[link_data["from_socket"]]
        to_node = nodes[link_data["to_node"]]
        to_socket = to_node.inputs[link_data["to_socket"]]

        node_tree.links.new(from_socket, to_socket)

    return node_tree

class GPT_OT_Execute(bpy.types.Operator):
    bl_idname = "gpt.execute"
    bl_label = "Execute"
    
    def execute(self, context):
        user_input = bpy.context.scene.gpt_input
        try:
            response = send_gpt_request(user_input)
          # Imprima a resposta no console
            self.report({"INFO"}, f"Resposta do ChatGPT: {response}")
        except ValueError as e:
            self.report({"ERROR"}, str(e))
            return {"CANCELLED"}

        try:
            node_tree_data = json.loads(response)
        except json.JSONDecodeError as e:
            error_msg = f"A resposta do ChatGPT não é um JSON válido. Erro: {e}"
            self.report({"ERROR"}, error_msg)
            return {"CANCELLED"}

        new_node_tree = create_geometry_nodes_from_dict("GeneratedGeometryNodesTree", node_tree_data)

        new_object = bpy.data.objects.new("GeneratedGeometryNodesObject", None)
        new_object.modifiers.new("GeneratedGeometryNodesModifier", "NODES")
        new_object.modifiers["GeneratedGeometryNodesModifier"].node_group = new_node_tree
        bpy.context.collection.objects.link(new_object)

        return {"FINISHED"}

class GPT_PT_Panel(bpy.types.Panel):
    bl_label = "ChatGPT Blender"
    bl_idname = "GPT_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GPT"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "gpt_api_key")
        layout.prop(context.scene, "gpt_input")
        layout.operator("gpt.execute")



def send_gpt_request(prompt):
    model_engine = "gpt-4"

    api_key = bpy.context.scene.gpt_api_key
    if not api_key:
        raise ValueError("A chave da API não foi fornecida.")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    instruction = '''
voce agora é um assitente do Blender que tem acesso as geometry nodes do Blender! voce vai responder as requisicoes do usuário como arquivos json que vao ser processados atraves dessas duas funcoes:
def create_geometry_nodes_from_dict(node_tree_name, node_tree_data):
    node_tree = bpy.data.node_groups.new(node_tree_name, "GeometryNodeTree")

    nodes = {}
    for node_data in node_tree_data["nodes"]:
        node = node_tree.nodes.new(node_data["type"])
        node.name = node_data["name"]
        node.location.x, node.location.y = node_data["location"]

        for prop_name, prop_value in node_data["properties"].items():
            if hasattr(node, prop_name):
                try:
                    setattr(node, prop_name, prop_value)
                except AttributeError:
                    pass

        nodes[node.name] = node

    for link_data in node_tree_data["links"]:
        from_node = nodes[link_data["from_node"]]
        from_socket = from_node.outputs[link_data["from_socket"]]
        to_node = nodes[link_data["to_node"]]
        to_socket = to_node.inputs[link_data["to_socket"]]

        node_tree.links.new(from_socket, to_socket)

    return node_tree

class GPT_OT_Execute(bpy.types.Operator):
    bl_idname = "gpt.execute"
    bl_label = "Execute"
    
    def execute(self, context):
        user_input = bpy.context.scene.gpt_input
        try:
            response = send_gpt_request(user_input)
        except ValueError as e:
            self.report({"ERROR"}, str(e))
            return {"CANCELLED"}
        
        try:
            node_tree_data = json.loads(response)
        except json.JSONDecodeError:
            self.report({"ERROR"}, "A resposta do ChatGPT não é um JSON válido.")
            return {"CANCELLED"}

        new_node_tree = create_geometry_nodes_from_dict("GeneratedGeometryNodesTree", node_tree_data)

        new_object = bpy.data.objects.new("GeneratedGeometryNodesObject", None)
        new_object.modifiers.new("GeneratedGeometryNodesModifier", "NODES")
        new_object.modifiers["GeneratedGeometryNodesModifier"].node_group = new_node_tree
        bpy.context.collection.objects.link(new_object)

        return {"FINISHED"}

    aqui está a lista de nos:
            Atributos e Informações sobre a Geometria:
        AttributeDomainSize
        AttributeStatistic
        BoundBox
        CollectionInfo
        CaptureAttribute
        FieldAtIndex
        FieldOnDomain
        InputMeshEdgeAngle
        InputMeshEdgeNeighbors
        InputMeshEdgeVertices
        InputMeshFaceArea
        InputMeshFaceIsPlanar
        InputMeshFaceNeighbors
        InputMeshIsland
        InputMeshVertexNeighbors
        InputNamedAttribute
        InputNormal
        InputPosition
        ObjectInfo
        Points
        PointsOfCurve
        Proximity
        Raycast
        SplineLength
        SplineParameter
        VertexOfCorner

    Curvas:
        CurveArc
        CurveEndpointSelection
        CurveHandleTypeSelection
        CurveLength
        CurveOfPoint
        CurvePrimitiveBezierSegment
        CurvePrimitiveCircle
        CurvePrimitiveLine
        CurvePrimitiveQuadrilateral
        CurveQuadraticBezier
        CurveSetHandles
        CurveSpiral
        CurveSplineType
        CurveStar
        CurveToMesh
        CurveToPoints
        DeformCurvesOnSurface
        FillCurve
        FilletCurve
        InputCurveHandlePositions
        InputCurveTilt
        JoinGeometry
        MeshToCurve
        OffsetCornerInFace
        OffsetPointInCurve
        ResampleCurve
        ReverseCurve
        SampleCurve
        SampleIndex
        SampleNearest
        SampleNearestSurface
        SetCurveHandlePositions
        SetCurveNormal
        SetCurveRadius
        SetCurveTilt
        SplitEdges
        StringToCurves
        SubdivideCurve
        TrimCurve

    Malhas:
        DuplicateElements
        EdgePathsToCurves
        EdgePathsToSelection
        EdgesOfCorner
        EdgesOfVertex
        ExtrudeMesh
        FaceOfCorner
        FlipFaces
        GeometryToInstance
        Group
        ImageTexture
        InputID
        InputIndex
        InputInstanceRotation
        InputInstanceScale
        InputMaterial
        InputMaterialIndex
        MergeByDistance
        MeshBoolean
        MeshCircle
        MeshCone
        MeshCube
        MeshCylinder
        MeshFaceSetBoundaries
        MeshGrid
        MeshIcoSphere

E para construir o nome da node corretamente, é preciso adicionar o prefixo "GeometryNode" antes do sufixo correspondente ao método desejado. Por exemplo, se quisermos utilizar o método "CurveArc", o nome completo da node seria "GeometryNodeCurveArc".

aqui estao input e output:
    NodeGroupInput(NodeInternal)
    NodeGroupOutput(NodeInternal)

    aqui esta um exemplo funcional que cria um cubo:
{
    "nodes": [
        {
            "name": "Input",
            "type": "NodeGroupInput",
            "location": [0, 0],
            "properties": {}
        },
        {
            "name": "Output",
            "type": "NodeGroupOutput",
            "location": [600, 0],
            "properties": {}
        },
        {
            "name": "MeshCube",
            "type": "GeometryNodeMeshCube",
            "location": [300, 0],
            "properties": {
                "size": 2.0
            }
        }
    ],
    "links": [
        {
            "from_node": "MeshCube",
            "from_socket": "Mesh",
            "to_node": "Output",
            "to_socket": "Geometry"
        }
    ]
}

sua resposta deve ser um json válido, responda somente em JSON com os nós e nada mais:

    '''

    messages = [{"role": "user", "content": instruction + prompt}]

    data = {
        "model": model_engine,
        "messages": messages,
    }

    import ssl
    ssl_context = ssl._create_unverified_context()

    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data).encode(), method="POST")

    try:
        with urllib.request.urlopen(req, context=ssl_context) as response:
            result = json.loads(response.read())
    except urllib.error.HTTPError as e:
        raise ValueError(f"HTTP error! status: {e.code}")

    message = result["choices"][0]["message"]["content"].strip()
    return message


def register():
    bpy.utils.register_class(GPT_OT_Execute)
    bpy.utils.register_class(GPT_PT_Panel)
    bpy.types.Scene.gpt_input = bpy.props.StringProperty(name="Input")
    bpy.types.Scene.gpt_api_key = bpy.props.StringProperty(name="API Key", description="Insira sua chave de API do OpenAI aqui", subtype="PASSWORD")

def unregister():
    bpy.utils.unregister_class(GPT_OT_Execute)
    bpy.utils.unregister_class(GPT_PT_Panel)
    del bpy.types.Scene.gpt_input

if __name__ == "__main__":
    register()

