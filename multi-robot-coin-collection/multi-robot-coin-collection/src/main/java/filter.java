import java.util.*;

class Point3D {
    int x, y, z;
    Point3D(int x, int y, int z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    @Override
    public boolean equals(Object o) {
        if (o instanceof Point3D p) {
            return this.x == p.x && this.y == p.y && this.z == p.z;
        }
        return false;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y, z);
    }
}

class MyLinkedList<T> {
    node<T> first;
    int size;

    public MyLinkedList() {
    }
    void addAll(ArrayList<T> list) {
        first = new node(list.get(0), null, null);
        size = 1;
        node<T> temp = first;
        for (int i = 1; i < list.size(); i++) {
            T point = list.get(i);
            node<T> newNode = new node(point, null, temp);
            temp.next = newNode;
            temp = newNode;
            size++;
        }
    }
    void remove(node<T> prev, node<T> next, int index) {
        if (prev != null) {
            prev.next = next;
        }
        if (next != null) {
            next.prev = prev;
        }
        size--;
        if (index == 0) {
            first = next;
        }
    }
    void add(node<T> prev, node<T> next, node<T> current, int index) {
        if (prev != null) {
            prev.next = current;
        }
        if (next != null) {
            next.prev = current;
        }
        size++;
        if (index == 0) {
            first = current;
        }
    }
}

class node<T> {
    T value;
    node<T> next;
    node<T> prev;

    public node(T value, node<T> next, node<T> prev) {
        this.value = value;
        this.next = next;
        this.prev = prev;
    }
}



public class filter {
    static int x, y, z;
    static int[][][] filter;
    static int totalCoins;
    static int robotsNum;
    static int max;
    static int maxCoins;

    static int findBestPath(ArrayList<Point3D> robots, ArrayList<Point3D> coins) {
        int maxCoin = Integer.MIN_VALUE;
        ArrayList<Integer> robotsRemained = new ArrayList<>();
        for (int i = 0; i < robots.size(); i++) {
            robotsRemained.add(max);
        }
        MyLinkedList<Point3D> coinsList = new MyLinkedList<>();
        coinsList.addAll(coins);
        MyLinkedList<Integer> remained = new MyLinkedList<>();
        remained.addAll(robotsRemained);
        MyLinkedList<Point3D> cells = new MyLinkedList<>();
        cells.addAll(robots);
        maxCoin = bestPath(coinsList, remained, maxCoin, 0, cells, max*robots.size(), 0,
                remained.first, cells.first);

        return Math.max(0, maxCoin);
    }




    static int bestPath (MyLinkedList<Point3D> notCollected, MyLinkedList<Integer> robotsRemained, int maxCoin, int index,
                         MyLinkedList<Point3D> lastCells, int point, int collected, node<Integer> remained,
                         node<Point3D> lastCell) {
        if (collected + notCollected.size > maxCoin) {
            boolean moved = false;
            node<Point3D> temp = notCollected.first;
            Point3D coin = temp.value;
            for (int i = 0; i < notCollected.size; i++) {
                int distance = distance(lastCell.value, coin);
                int newPoint = point - distance + 1;

                if (distance <= remained.value && newPoint > maxCoin) {
                    if (collected + 1 >= totalCoins) {
                        System.out.println(totalCoins+maxCoins);
                        System.exit(0);
                    } else if (collected + 1 >= max * robotsNum) {
                        System.out.println( max * robotsNum + maxCoins);
                        System.exit(0);
                    }
                    moved = true;


                    // store data
                    int oldIndex = index;
                    int oldRemained = remained.value;
                    Point3D oldCell = lastCell.value;
                    node<Point3D> prevCoin = temp.prev;
                    node<Point3D> nextCoin = temp.next;
                    node<Point3D> prevCell = lastCell.prev;
                    node<Point3D> nextCell = lastCell.next;
                    node<Integer> prevRem = remained.prev;
                    node<Integer> nextRem = remained.next;

                    // new data
                    remained.value = oldRemained-distance;
                    lastCell.value = coin;
                    notCollected.remove(prevCoin, nextCoin, i);
                    node<Point3D> newCell = (nextCell != null) ? nextCell : lastCells.first;
                    node<Integer> newRem = (nextCell != null) ? nextRem : robotsRemained.first;


                    if (oldRemained - distance == 0) {
                        if (lastCells.size == 1) {
                            maxCoin = Math.max(maxCoin, collected+1);
                        } else {
                            // update data
                            lastCells.remove(prevCell, nextCell, index);
                            robotsRemained.remove(prevRem, nextRem, index);
                            if (lastCells.size == 1 || index == lastCells.size) {
                                index = 0;
                            }

                            maxCoin = bestPath(notCollected, robotsRemained, maxCoin, index, lastCells, newPoint,
                                    collected+1, newRem, newCell);

                            // undo changes
                            index = oldIndex;
                            lastCells.add(prevCell, nextCell, lastCell, index);
                            robotsRemained.add(prevRem, nextRem, remained, index);
                        }
                    }

                    else {
                        index = (index < lastCells.size - 1) ? index + 1 : 0;

                        maxCoin = bestPath(notCollected, robotsRemained, maxCoin, index, lastCells, newPoint,
                                collected + 1, newRem, newCell);

                        // undo changes
                        index = oldIndex;

                    }

                    // undo changes
                    remained.value = oldRemained;
                    lastCell.value = oldCell;
                    notCollected.add(prevCoin, nextCoin, temp, i);

                }

                temp = temp.next;
                if (temp != null) {
                    coin = temp.value;
                }


            }
            if (!moved) {

                // store data
                node<Point3D> prevCell = lastCell.prev;
                node<Point3D> nextCell = lastCell.next;
                node<Integer> prevRem = remained.prev;
                node<Integer> nextRem = remained.next;

                if (lastCells.size == 1) {
                    maxCoin = Math.max(maxCoin, collected);
                } else {
                    lastCells.remove(prevCell, nextCell, index);
                    robotsRemained.remove(prevRem, nextRem, index);
                    int oldIndex = index;
                    if (lastCells.size == 1 || index == lastCells.size) {
                        index = 0;
                    }

                    node<Point3D> newCell = (nextCell != null) ? nextCell : lastCells.first;
                    node<Integer> newRem = (nextCell != null) ? nextRem : robotsRemained.first;

                    maxCoin = bestPath(notCollected, robotsRemained, maxCoin, index, lastCells, point- remained.value,
                            collected, newRem, newCell);


                    // undo changes
                    index = oldIndex;
                    robotsRemained.add(prevRem, nextRem, remained, index);
                    lastCells.add(prevCell, nextCell, lastCell, index);

                }
            }
        }
        return maxCoin;
    }

    static int distance(Point3D a, Point3D b) {
        return Math.abs(a.x - b.x) + Math.abs(a.y - b.y) + Math.abs(a.z - b.z);
    }


    static ArrayList<Point3D> setRobots(int n) {
        ArrayList<Point3D> robots = new ArrayList<>();
        int max = Integer.MIN_VALUE;
        for (int i = 1; i <= n; i++) {
            int rz = i / (x * y);
            int remaining = i % (x * y);
            int ry;
            int rx;
            if (remaining != 0) {
                rz += 1;
                ry = remaining / x;
                remaining %= x;
                if (remaining != 0) {
                    rx = remaining;
                    ry += 1;
                }
                else {
                    rx = x;
                }
            }
            else {
                ry = y;
                rx = x;
            }
            if (rx+ry+rz > max) {
                max = rx+ry+rz;
            }
            robots.add(new Point3D(rx, ry, rz));
        }
        robots.add(new Point3D(max, 0,0));
        return robots;
    }




    static void addCoins(ArrayList<Point3D> coins, int robots, int maxCoins, int max) {
        for (int zi = 1; zi <= z; zi++) {
            for (int yi = 1; yi <= y; yi++) {
                for (int xi = 1; xi <= x; xi++) {
                    if (filter[zi][yi][xi] == 1) {
                        if ((zi - 1) * (x * y) + (yi - 1) * x + xi > robots) {
                            if (zi+yi+xi <= max) {
                                coins.add(new Point3D(xi, yi, zi));
                            }
                        } else {
                            maxCoins++;
                        }
                    }
                }
            }
        }
    }



    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        x = scanner.nextInt();
        y = scanner.nextInt();
        z = scanner.nextInt();

        filter = new int[z + 1][y + 1][x + 1];
        maxCoins = 0;
        ArrayList<Point3D> coins = new ArrayList<>();
        int counter = 0;

        // get cells
        for (int zi = 1; zi <= z; zi++) {
            for (int yi = 1; yi <= y; yi++) {
                for (int xi = 1; xi <= x; xi++) {
                    filter[zi][yi][xi] = scanner.nextInt();
                    if (filter[zi][yi][xi] == 1) {
                        if ((zi - 1) * (x * y) + (yi - 1) * x + xi <= n) {
                            maxCoins++;
                        }
                        counter++;
                    }
                }
            }
        }
        if (n >= x * y || n >= x * z || n >= y * z) {
            System.out.println(counter);
        }

        else if (n == 0) {
            System.out.println(0);
        }


        else {
            if (z != 0 && y != 0 && x != 0) {
                // set robots
                ArrayList<Point3D> robots = setRobots(n);
                max = Math.max(Math.max(x, y), z);
                int maxSum = robots.get(robots.size() - 1).x;
                robots.remove(robots.size() - 1);
                robotsNum = robots.size();

                // add coins
                addCoins(coins, n, maxCoins, max + maxSum);
                Comparator<Point3D> comparator = new Comparator<>() {
                    @Override
                    public int compare(Point3D o1, Point3D o2) {
                        return (o1.x + o1.y + o1.z) - (o2.x + o2.y + o2.z);
                    }
                };
                coins.sort(comparator);

                totalCoins = coins.size();

                if (robots.size() > 0 && coins.size() > 0) {
                    maxCoins += findBestPath(robots, coins);
                }



            }

            System.out.println(maxCoins);
        }


    }
}