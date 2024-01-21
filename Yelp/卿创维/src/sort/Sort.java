/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package sort;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 *
 * @author ricardo
 */
public class Sort {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        
        int[] numberArray = {1,1,1,2,2,2,2,3,3,0};
        Map<Integer,Data> dataMap = new HashMap<Integer, Data>();
        for(int i : numberArray) {
            if(dataMap.containsKey(i)) {
                Data data = dataMap.get(i);
                data.setCount(data.getCount() + 1);
                dataMap.put(i, data);
            }else {
                Data data = new Data(i,1);
                
                dataMap.put(i, data);
            }
            
        }
        
        List<Data> dataList = new ArrayList<>();
        for(Data d : dataMap.values()){
            dataList.add(d);
            System.out.println("number:" + d.getNumber()+";count:" + d.getCount());
        }
        heapSort(dataList);
        System.out.println("-------");
        for(Data d : dataList) {
            System.out.println("number:" + d.getNumber()+";count:" + d.getCount());
        }
        
        
    }
    
    private static void heapSort(List<Data> dataList) { 
		// 将待排序的序列构建成一个大顶堆
        for (int i = dataList.size() / 2; i >= 0; i--){ 
                heapAdjust(dataList, i, dataList.size()); 
        }

        // 逐步将每个最大值的根节点与末尾元素交换，并且再调整二叉树，使其成为大顶堆
        for (int i = dataList.size() - 1; i > 0; i--) { 
                swap(dataList, 0, i); // 将堆顶记录和当前未经排序子序列的最后一个记录交换
                heapAdjust(dataList, 0, i); // 交换之后，需要重新检查堆是否符合大顶堆，不符合则要调整
        }
    }
    
    private static void heapAdjust(List<Data> dataList, int i, int n) {
        int child;
        int father; 
        for (father = i; leftChild(i) < n; i = child) {
                child = leftChild(i);

                // 如果左子树小于右子树，则需要比较右子树和父节点
                if (child != n - 1 && dataList.get(child).getCount() > dataList.get(child+1).getCount()) {
                        child++; // 序号增1，指向右子树
                }

                // 如果父节点小于孩子结点，则需要交换
                if (dataList.get(father).getCount() > dataList.get(child).getCount()) {
                    Data d1 = dataList.get(child);
                    Data d2 = dataList.get(i);
                    dataList.set(i, d1);
                    dataList.set(child, d2);
                    //System.out.println("swap--------");
                    
                } else {
                        break; // 大顶堆结构未被破坏，不需要调整
                }
        }
        //Data d = dataList.get(father);
        //dataList.set(i, d);
        
    }
 
    // 获取到左孩子结点
    private static int leftChild(int i) {
        return 2 * i + 1;
    }

    // 交换元素位置
    private static void swap(List<Data> dataList, int index1, int index2) {

        Data tmp = dataList.get(index1);
        //int tmp = arr[index1];
        
        dataList.set(index1, dataList.get(index2));
        dataList.set(index2, tmp);
        //arr[index1] = arr[index2];
        //arr[index2] = tmp;

    }


}
