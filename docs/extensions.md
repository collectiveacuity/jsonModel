# Extensions
_a package of extensions to a jsonModel class object_
## tabulate
### 
**Import:**  
jsonmodel.extensions  
### 
**Initialize::**

    from jsonmodel.extensions import tabulate
    json_model = jsonModel(sample_schema)
    tabulate(json_model)

### 
**Signature:**  
tabulate(self, format="html", syntax="")
### 
**Description:**  
a function to create a table from the class model keyMap  
<table>
<thead>
<tr><th>Argument  </th><th>Type  </th><th>Required  </th><th>Default  </th><th>Description                             </th></tr>
</thead>
<tbody>
<tr><td>self      </td><td>object</td><td>Yes       </td><td>None     </td><td>                                        </td></tr>
<tr><td>format    </td><td>str   </td><td>          </td><td>&quot;html&quot;   </td><td>string with format for table output     </td></tr>
<tr><td>syntax    </td><td>str   </td><td>          </td><td>&quot;&quot;       </td><td>[optional] string with linguistic syntax</td></tr>
</tbody>
</table>
