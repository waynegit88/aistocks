<template>

  <div class="home">

    <el-row display="margin-top:10px">

      <el-input v-model="name" placeholder="please input user name" style="display:inline-table; width: 30%; float:left"></el-input>
      <el-input v-model="password" placeholder="please input password" style="display:inline-table; width: 30%; float:left"></el-input>
      <el-input v-model="email" placeholder="please input email" style="display:inline-table; width: 30%; float:left"></el-input>

      <el-button type="primary" @click="add_user()" style="float:left; margin: 2px;">AddUser</el-button>

    </el-row>

    <el-row>

      <el-table :data="userList" style="width: 100%" border>

        <el-table-column prop="id" label="编号" min-width="100">

          <template slot-scope="scope"> {{ scope.row.pk }} </template>

        </el-table-column>

        <el-table-column prop="name" label="书名" min-width="100">

          <template slot-scope="scope"> {{ scope.row.fields.name }} </template>

        </el-table-column>

        <el-table-column prop="c_time" label="添加时间" min-width="100">

          <template slot-scope="scope"> {{ scope.row.fields.c_time }} </template>

        </el-table-column>

      </el-table>

    </el-row>

  </div>
</template>



<script>

export default {

  name: 'home',

  data () {

    return {

      name: '',
      password: '',
      email: '',

      userList: []

    }

  },

  mounted: function () {

    this.show_users()

  },

  methods: {

    add_user () {

      this.$http.get('http://127.0.0.1:8000/api/add_user?name=' + this.name + '&password=' + this.password + '&email=' + this.email)

        .then((response) => {

          var res = JSON.parse(response.bodyText)

          if (res.error_num === 0) {

            this.show_users()

          } else {

            this.$message.error('新增书籍失败，请重试')

            console.log(res['msg'])

          }

        })

    },

    show_users () {

      this.$http.get('http://127.0.0.1:8000/api/show_users')

        .then((response) => {

          var res = JSON.parse(response.bodyText)

          console.log(res)

          if (res.error_num === 0) {

            this.userList = res['list']

          } else {

            this.$message.error('查询书籍失败')

            console.log(res['msg'])

          }

        })

    }

  }

}

</script>



<!-- Add "scoped" attribute to limit CSS to this component only -->

<style scoped>

  h1, h2 {

    font-weight: normal;

  }



  ul {

  list-style-type: none;

  padding: 0;

}



li {

  display: inline-block;

  margin: 0 10px;

}



a {

  color: #42b983;

}

</style>
