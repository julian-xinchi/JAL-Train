

在数学和物理学中，向量（vector）通常用以下方式表示：

---

### 1. **手写体表示**
在手写时，向量通常用字母上方加箭头表示：
\[
\vec{v}
\]
其中，\( v \) 是向量的名称。

---

### 2. **印刷体表示**
在印刷体中，向量通常用粗体字母表示：
\[
\mathbf{v}
\]

---

### 3. **矩阵表示**
向量也可以表示为列向量或行向量的形式：
- 列向量：
\[
\mathbf{v} = \begin{pmatrix} v_1 \\ v_2 \\ \vdots \\ v_n \end{pmatrix}
\]
- 行向量：
\[
\mathbf{v} = \begin{pmatrix} v_1 & v_2 & \cdots & v_n \end{pmatrix}
\]

---

### 4. **分量表示**
向量可以用其分量表示。例如，在三维空间中：
\[
\mathbf{v} = (v_x, v_y, v_z)
\]
或者：
\[
\mathbf{v} = v_x \mathbf{i} + v_y \mathbf{j} + v_z \mathbf{k}
\]
其中，\( \mathbf{i} \)、\( \mathbf{j} \)、\( \mathbf{k} \) 是坐标轴的单位向量。

---

### 5. **LaTeX 中的向量表示**
在 LaTeX 或 Sphinx 的 `.. math::` 环境中，可以使用以下命令表示向量：
- 箭头表示：
  ```latex
  \vec{v}
  ```
  示例：
  ```rst
  .. math::

     \vec{v} = (v_1, v_2, v_3)
  ```

- 粗体表示：
  ```latex
  \mathbf{v}
  ```
  示例：
  ```rst
  .. math::

     \mathbf{v} = (v_1, v_2, v_3)
  ```

- 单位向量表示：
  ```latex
  \hat{i}, \hat{j}, \hat{k}
  ```
  示例：
  ```rst
  .. math::

     \mathbf{v} = v_1 \hat{i} + v_2 \hat{j} + v_3 \hat{k}
  ```

---

### 6. **向量的运算**
向量常见的运算包括：
- **加法**：
  \[
  \mathbf{u} + \mathbf{v} = (u_1 + v_1, u_2 + v_2, u_3 + v_3)
  \]
- **点积（内积）**：
  \[
  \mathbf{u} \cdot \mathbf{v} = u_1 v_1 + u_2 v_2 + u_3 v_3
  \]
- **叉积（外积）**：
  \[
  \mathbf{u} \times \mathbf{v} = \begin{pmatrix}
  \mathbf{i} & \mathbf{j} & \mathbf{k} \\
  u_1 & u_2 & u_3 \\
  v_1 & v_2 & v_3
  \end{pmatrix}
  \]

---

### 示例代码
在 Sphinx 的 `.. math::` 环境中，可以这样表示向量：
```rst
.. math::

   \mathbf{v} = \begin{pmatrix} v_1 \\ v_2 \\ v_3 \end{pmatrix}
   \quad
   \mathbf{u} \cdot \mathbf{v} = u_1 v_1 + u_2 v_2 + u_3 v_3
```

---

希望这些表达方式对你有帮助！
