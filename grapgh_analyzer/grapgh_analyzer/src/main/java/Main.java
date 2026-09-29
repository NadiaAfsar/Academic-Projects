import java.util.*;

class Vertex {
    private String ID;
    private double weight;
    private ArrayList<String> edges;

    public String getID() {
        return ID;
    }

    public Vertex(String ID, double weight) {
        this.ID = ID;
        this.weight = weight;
        edges = new ArrayList<>();
    }

    public ArrayList<String> getEdges() {
        return edges;
    }

    public void setWeight(double weight) {
        this.weight = weight;
    }

    public double getWeight() {
        return weight;
    }
}
class Edge {
    private String start;
    private String end;
    private double weight;

    public Edge(String start, String end, double weight) {
        this.start = start;
        this.end = end;
        this.weight = weight;
    }

    public void setWeight(double weight) {
        this.weight = weight;
    }

    public double getWeight() {
        return weight;
    }

    public String getStart() {
        return start;
    }

    public String getEnd() {
        return end;
    }
}
class Graph {
    private String ID;
    private HashMap<String, Vertex> vertexesMap;
    private HashMap<String, Edge> edgesMap;

    public String getID() {
        return ID;
    }


    public HashMap<String, Vertex> getVertexesMap() {
        return vertexesMap;
    }

    public HashMap<String, Edge> getEdgesMap() {
        return edgesMap;
    }

    public Graph(String ID) {
        this.ID = ID;
        vertexesMap = new HashMap<>();
        edgesMap = new HashMap<>();
    }
}

public class Main {
    private static boolean isNewGraph(String[] command, HashMap<String, Graph> graphs) {
        if (command.length == 2) {
            String ID = command[1];
            try {
                int IDNum = Integer.parseInt(ID);
                if (IDNum >= 10) {
                    return graphs.get(ID) == null;
                }
            }
            catch (Exception e) {
                return false;
            }
        }
        return false;
    }
    private static boolean isAddVertex(String[] command, HashMap<String, Graph> graphs){
        if (command.length == 4) {
            try {
                int ID = Integer.parseInt(command[1]);
                int verId = Integer.parseInt(command[2]);
                Double.parseDouble(command[3]);
                if (verId >= 10000000) {
                    Graph graph = graphs.get(command[1]);
                    if (graph != null) {
                        return graph.getVertexesMap().get(command[2]) == null;
                    }
                }
            }
            catch (Exception e) {
                return false;
            }
        }
        return false;
    }
    private static void addVertex(String[] words, HashMap<String, Graph> graphs) {
        double vertexWeight = Double.parseDouble(words[3]);
        Graph graph = graphs.get(words[1]);
        graph.getVertexesMap().put(words[2], new Vertex(words[2], vertexWeight));
    }
    private static boolean isAddEdge(String[] command, HashMap<String, Graph> graphs) {
        if (command.length == 5) {
            try {
                int ID = Integer.parseInt(command[1]);
                int stID = Integer.parseInt(command[2]);
                int enID = Integer.parseInt(command[3]);
                Double.parseDouble(command[4]);
                String edgeID = command[2]+command[3];
                Graph graph = graphs.get(command[1]);
                if (graph != null) {
                    if (stID != enID) {
                        Map<String, Vertex> vertexMap = graph.getVertexesMap();
                        if (vertexMap.get(command[2]) != null) {
                            if (vertexMap.get(command[3]) != null) {
                                return graph.getEdgesMap().get(edgeID) == null;
                            }
                        }
                    }
                }
            }
            catch (Exception e) {
                return false;
            }
        }
        return false;
    }
    private static void addEdge(String[] words, HashMap<String, Graph> graphs) {
        double weight = Double.parseDouble(words[4]);
        String ID = words[2]+words[3];
        Graph graph = graphs.get(words[1]);
        graph.getEdgesMap().put(ID, new Edge(words[2], words[3], weight));
        graph.getVertexesMap().get(words[2]).getEdges().add(ID);
        graph.getVertexesMap().get(words[3]).getEdges().add(ID);
    }
    private static boolean isDelVertex(String[] command, HashMap<String, Graph> graphs) {
        if (command.length == 3) {
            try {
                Integer.parseInt(command[1]);
                Integer.parseInt(command[2]);
                Graph graph = graphs.get(command[1]);
                if (graph != null) {
                    return graph.getVertexesMap().get(command[2]) != null;
                }
            }
            catch (Exception e) {
                return false;
            }
        }
        return false;
    }
    private static void delVertex(String[] words, HashMap<String, Graph> graphs) {
        Graph graph = graphs.get(words[1]);
        ArrayList<String> edges = graph.getVertexesMap().get(words[2]).getEdges();
        for (int i = 0; i < edges.size(); i++) {
            graph.getEdgesMap().remove(edges.get(i));
        }
        graph.getVertexesMap().remove(words[2]);
    }
    private static boolean isDelEdge(String[] command, HashMap<String, Graph> graphs) {
        if (command.length == 4) {
            try {
                int ID = Integer.parseInt(command[1]);
                int stID = Integer.parseInt(command[2]);
                int enID = Integer.parseInt(command[3]);
                Graph graph = graphs.get(command[1]);
                if (graph != null) {
                    return graph.getEdgesMap().get(command[2]+command[3]) != null;
                }
            }
            catch (Exception e) {
                return false;
            }
        }
        return false;
    }
    private static void delEdge(String[] words, HashMap<String, Graph> graphs) {
        Graph graph = graphs.get(words[1]);
        String ID = words[2]+words[3];
        graph.getEdgesMap().remove(ID);
    }
    private static boolean isEditVertex(String[] command, HashMap<String, Graph> graphs) {
        if (command.length == 4) {
            try {
                int ID = Integer.parseInt(command[1]);
                int verID = Integer.parseInt(command[2]);
                Double.parseDouble(command[3]);
                Graph graph = graphs.get(command[1]);
                if (graph != null) {
                    return graph.getVertexesMap().get(command[2]) != null;
                }
            }
            catch (Exception e) {
                return false;
            }
        }
        return false;
    }
    private static void editVertex(String[] words, HashMap<String, Graph> graphs) {
        double weight = Double.parseDouble(words[3]);
        graphs.get(words[1]).getVertexesMap().get(words[2]).setWeight(weight);
    }
    private static boolean isEditEdge(String[] command, HashMap<String, Graph> graphs) {
        if (command.length == 5) {
            try {
                int ID = Integer.parseInt(command[1]);
                int stID = Integer.parseInt(command[2]);
                int enID = Integer.parseInt(command[3]);
                Double.parseDouble(command[4]);
                Graph graph = graphs.get(command[1]);
                if (graph != null) {
                    return graph.getEdgesMap().get(command[2]+command[3]) != null;
                }
            }
            catch (Exception e) {
                return false;
            }
        }
        return false;
    }
    private static void editEdge(String[] words, HashMap<String, Graph> graphs) {
        int graphID = Integer.parseInt(words[1]);
        int stID = Integer.parseInt(words[2]);
        int enID = Integer.parseInt(words[3]);
        double weight = Double.parseDouble(words[4]);
        graphs.get(words[1]).getEdgesMap().get(words[2]+words[3]).setWeight(weight);
    }
    private static boolean isShowGraph(String[] command, HashMap<String, Graph> graphs) {
        if (command.length == 2) {
            try {
                int ID = Integer.parseInt(command[1]);
                return graphs.get(command[1]) != null;
            }
            catch (Exception e) {
                return false;
            }
        }
        return false;
    }
    private static void showGraph(Graph graph) {
        HashMap<String, Vertex> vertexTreeMap = graph.getVertexesMap();
        HashMap<String, Edge> edgeTreeMap = graph.getEdgesMap();
        ArrayList<String> vertices = new ArrayList<>(vertexTreeMap.keySet());
        ArrayList<String> edges = new ArrayList<>(edgeTreeMap.keySet());
        Collections.sort(vertices);
        Collections.sort(edges);
        int n = vertexTreeMap.size();
        int m = edgeTreeMap.size();
        System.out.println(graph.getID()+" "+n+" "+m);
        for (int i = 0; i < n; i++) {
            Vertex vertex = vertexTreeMap.get(vertices.get(i));
            if (vertex != null) {
                System.out.print(graph.getID()+" "+vertex.getID()+" ");
                System.out.printf("%.6f", vertex.getWeight());
                System.out.println();
            }
        }
        for (int i = 0; i < m; i++) {
            Edge edge = edgeTreeMap.get(edges.get(i));
            if (edge != null) {
                System.out.print(graph.getID()+" "+edge.getStart()+" "+edge.getEnd()+" ");
                System.out.printf("%.6f", edge.getWeight());
                System.out.println();
            }
        }
    }
    public static void main(String[] args) {
        HashMap<String, Graph> graphs = new HashMap<>();
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        scanner.nextLine();
        for (int i = 0; i < n; i++) {
            String command = scanner.nextLine();
            String[] words = command.split(" ");
            boolean commandAccepted = false;
            if (words[0].equals("NEW_GRAPH")) {
                if (isNewGraph(words, graphs)) {
                    graphs.put(words[1], new Graph(words[1]));
                    commandAccepted = true;
                }
            }
            else if (words[0].equals("ADD_VERTEX")) {
                if (isAddVertex(words, graphs)) {
                    addVertex(words, graphs);
                    commandAccepted = true;
                }
            }
            else if (words[0].equals("ADD_EDGE")) {
                if (isAddEdge(words, graphs)) {
                    addEdge(words, graphs);
                    commandAccepted = true;
                }
            }
            else if (words[0].equals("DEL_VERTEX")) {
                if (isDelVertex(words, graphs)) {
                    delVertex(words, graphs);
                    commandAccepted = true;
                }
            }
            else if (words[0].equals("DEL_EDGE")) {
                if (isDelEdge(words, graphs)) {
                    delEdge(words, graphs);
                    commandAccepted = true;
                }
            }
            else if (words[0].equals("EDIT_VERTEX")) {
                if (isEditVertex(words, graphs)) {
                    editVertex(words, graphs);
                    commandAccepted = true;
                }
            }
            else if (words[0].equals("EDIT_EDGE")) {
                if (isEditEdge(words, graphs)) {
                    editEdge(words, graphs);
                    commandAccepted = true;
                }
            }
            else if (words[0].equals("SHOW_GRAPH")) {
                if (isShowGraph(words, graphs)) {
                    showGraph(graphs.get(words[1]));
                    commandAccepted = true;
                }
            }
            if (!commandAccepted) {
                System.out.println("INVALID COMMAND");
            }
        }
    }
}

