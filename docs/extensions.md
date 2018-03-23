<table>
<thead>
<tr><th>Field                              </th><th>Datatype        </th><th>Required  </th><th>Examples  </th><th>Conditions        </th></tr>
</thead>
<tbody>
<tr><td>string_fields                      </td><td>string          </td><td>          </td><td>""        </td><td>                  </td></tr>
<tr><td>similar_string                     </td><td>string          </td><td>          </td><td>""        </td><td>                  </td></tr>
<tr><td>number_fields                      </td><td>number          </td><td>          </td><td>0.0       </td><td>                  </td></tr>
<tr><td>similar_number                     </td><td>number          </td><td>          </td><td>0         </td><td>integer_data: true</td></tr>
<tr><td>boolean_fields                     </td><td>boolean         </td><td>          </td><td>false     </td><td>                  </td></tr>
<tr><td>similar_boolean                    </td><td>boolean         </td><td>          </td><td>false     </td><td>                  </td></tr>
<tr><td>map_fields                         </td><td>object          </td><td>          </td><td>{...}     </td><td>extra_fields: true</td></tr>
<tr><td>similar_map                        </td><td>object          </td><td>          </td><td>{...}     </td><td>extra_fields: true</td></tr>
<tr><td>list_fields                        </td><td>array of strings</td><td>          </td><td>[ "" ]    </td><td>                  </td></tr>
<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;<i>item</i></td><td>string          </td><td>          </td><td>""        </td><td>                  </td></tr>
<tr><td>similar_list                       </td><td>array of strings</td><td>          </td><td>[ "" ]    </td><td>                  </td></tr>
<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;<i>item</i></td><td>string          </td><td>          </td><td>""        </td><td>                  </td></tr>
<tr><td>null_fields                        </td><td>null            </td><td>          </td><td>null      </td><td>                  </td></tr>
<tr><td>similar_null                       </td><td>null            </td><td>          </td><td>null      </td><td>                  </td></tr>
</tbody>
</table>